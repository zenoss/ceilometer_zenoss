##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014-2016, all rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

try:
    # should work up to Kilo
    from ceilometer.openstack.common import log
except ImportError:
    try:
        # should work starting from Liberty
        from oslo_log import log
    except ImportError:
        import logging as log

try:
    # should work up to Kilo
    from oslo.config import cfg
except ImportError:
    try:
        # should work starting from Liberty
        from oslo_config import cfg
    except ImportError:
        # should not reach here
        raise ImportError('Could not import cfg from oslo.config, oslo_config.')

LOG = log.getLogger(__name__)

from ceilometer import dispatcher

from kombu import Connection
from kombu.entity import Exchange
from kombu.messaging import Producer

from contextlib import contextmanager
import datetime
import os
import os.path
import socket
import sys
import time
import threading

zenoss_dispatcher_opts = [
    cfg.StrOpt('zenoss_device',
               default=None,
               help='Zenoss device name for this openstack environment.'),
    cfg.StrOpt('amqp_hostname',
               default=None,
               help='Zenoss AMQP Host'),
    cfg.IntOpt('amqp_port',
               default=None,
               help='Zenoss AMQP Port'),
    cfg.StrOpt('amqp_userid',
               default=None,
               help='Zenoss AMQP UserID'),
    cfg.StrOpt('amqp_password',
               default=None,
               help='Zenoss AMQP Password'),
    cfg.StrOpt('amqp_virtual_host',
               default=None,
               help='Zenoss AMQP Virtual Host'),
    cfg.IntOpt('amqp_max_retries',
               default=5,
               help='Maximum number of times to retry when (re)connecting to AMQP.'),
    cfg.IntOpt('amqp_retry_interval_start',
               default=1,
               help='Seconds to sleep when retrying'),
    cfg.IntOpt('amqp_retry_interval_step',
               default=1,
               help='Seconds to add to the sleep interval on each retry)'),
    cfg.IntOpt('amqp_retry_interval_max',
               default=5,
               help='Maximum number of seconds to sleep between retries'),
    cfg.IntOpt('zenoss_heartbeat_interval',
               default=30,
               help='Seconds to sleep between heartbeat messages sent to zenoss.'),
    cfg.IntOpt('amqp_error_disable',
               default=30,
               help='Seconds to disable the dispatcher when AMQP connectivity errors occur.'),
]

cfg.CONF.register_opts(zenoss_dispatcher_opts, group="dispatcher_zenoss")


try:
    from ceilometer.dispatcher import MeterDispatcherBase, EventDispatcherBase

    class ZenossDispatcherBase(MeterDispatcherBase, EventDispatcherBase):
        '''
            Inherit from both MeterDispatcherBase, EventDispatcherBase
            for Mitaka and newer
        '''

    # In newer versions of ceilometer, the oslo notifications are processed by
    # ceilometer-collector using the threading executor, so dispatcher methods
    # are invoked within a thread pool.   Therefore, connection
    # pooling should be managed appropriately, using python thread
    # synchronization primitives.
    from pool import Pool
    from threading import Semaphore

except ImportError:
    # On versions prior to mitaka, the oslo notifications are processed by
    # ceilometer-collector using the eventlet executor, so an eventlet-aware
    # connection pooler is used.
    from eventlet.pools import Pool
    from eventlet.semaphore import Semaphore

    class ZenossDispatcherBase(dispatcher.Base):
        '''
            Inherit from dispatcher.Base
            for Liberty and older
        '''


# Basic connection pooling for our amqp producers and sessions, used for sending
# AMQP messages to zenoss.

class AMQPConnection(object):

    conf = None
    connection = None
    producer = None
    needs_reconnect = False

    def __init__(self, conf, exchange):
        self.conf = conf
        self.exchange = exchange
        self.reconnect()

    def reconnect(self):
        self.needs_reconnect = False

        LOG.info("Opening new AMQP connection to amqp://%s@%s:%s%s (%s)" % (
            self.conf.amqp_userid, self.conf.amqp_hostname, self.conf.amqp_port, self.conf.amqp_virtual_host, self.exchange.name))

        if self.connection:
            self.connection.release()

        try:
            self.connection = Connection(
                hostname=self.conf.amqp_hostname,
                userid=self.conf.amqp_userid,
                password=self.conf.amqp_password,
                virtual_host=self.conf.amqp_virtual_host,
                port=self.conf.amqp_port)

            channel = self.connection.channel()   # get a new channel
            self.producer = Producer(channel, self.exchange, auto_declare=False)
        except Exception, e:
            LOG.error("Error opening AMQP connection: %s" % e)
            self.needs_reconnect = True


class AMQPPool(Pool):
    def __init__(self, conf, *args, **kwargs):
        self.conf = conf
        super(AMQPPool, self).__init__(*args, **kwargs)

    def create(self):
        exchange = Exchange('zenoss.openstack.ceilometer', type='topic')
        return AMQPConnection(self.conf, exchange)

    @contextmanager
    def item(self):
        obj = self.get()
        try:
            yield obj
        finally:
            self.put(obj)

_pool_create_sem = Semaphore()


class Heartbeat(threading.Thread):
    name = "dispatcher_zenoss heartbeat"
    daemon = True
    disable_until = None

    def __init__(self, conf):
        super(Heartbeat, self).__init__()

        self.conf = conf
        exchange = Exchange('zenoss.openstack.heartbeats', type='topic')
        self.connection = AMQPConnection(self.conf, exchange)

        self.hostname = socket.gethostname()
        self.processname = os.path.basename(sys.argv[0])
        self.processid = os.getpid()

    def run(self):
        # Start sending heartbeats to zenoss
        conf = self.conf

        while True:
            if not self.enabled:
                time.sleep(conf.zenoss_heartbeat_interval)
                continue

            try:
                if self.connection.needs_reconnect:
                    self.connection.reconnect()
                    if self.connection.needs_reconnect:
                        LOG.error("Unable to establish AMQP connection, unable to send heartbeats at this time. "
                                  "Check AMQP connectivity and authentication credentials")
                        self.disable_for(conf.amqp_error_disable)
                        continue
                    self.reenable()

                if self.enabled:
                    self.send_heartbeat()

            except Exception, e:
                LOG.error("Exception encountered during heartbeat processing: %s", e)
                self.disable_for(conf.amqp_error_disable)

            time.sleep(conf.zenoss_heartbeat_interval)

    @property
    def enabled(self):
        if self.disable_until is None:
            return True
        else:
            if self.disable_until < datetime.datetime.now():
                self.reenable()
                return True
            return False

    def disable_for(self, seconds):
        LOG.info("Disabling %s for %d seconds", self, seconds)
        self.disable_until = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    def reenable(self):
        LOG.info("Re-Enabling %s", self)
        self.disable_until = None

    def send_heartbeat(self):
        conf = self.conf

        routing_key = 'zenoss.openstack.heartbeat.%s.%s.%s' % (
            conf.zenoss_device,
            self.hostname,
            self.processname
        )

        heartbeat_message = dict(
            timestamp=int(time.time()),
            hostname=self.hostname,
            processname=self.processname,
            processid=self.processid
        )

        def errback(exc, interval):
            LOG.warning("Couldn't publish heartbeat message: %r. Retry in %ds" % (exc, interval))

        publish_with_retry = self.connection.connection.ensure(
            self.connection.producer,
            self.connection.producer.publish,
            errback=errback,
            max_retries=conf.amqp_max_retries,
            interval_start=conf.amqp_retry_interval_start,
            interval_step=conf.amqp_retry_interval_step,
            interval_max=conf.amqp_retry_interval_max,
            )

        LOG.info("Sending heartbeat to %s" % routing_key)
        publish_with_retry(
            heartbeat_message,
            serializer='json',
            routing_key=routing_key,
            headers={'x-message-ttl': 600000}  # 10 minutes
        )


class ZenossDispatcher(ZenossDispatcherBase):
    '''

    [dispatcher_zenoss]

    # Name of the device in zenoss for this openstack environment
    zenoss_device=myopenstack
    amqp_hostname=zenosshost
    amqp_port=5672
    amqp_userid=zenoss
    amqp_password=zenoss
    amqp_virtual_host=/zenoss

    To enable this dispatcher, the following section needs to be present in
    ceilometer.conf file

    [collector]
    dispatchers = zenoss

    (Note that other dispatchers may be listed on their own lines as well,
     such as dispatchers = database)
    '''

    pool = None
    heartbeat = None
    disable_until = None

    def __init__(self, conf):
        super(ZenossDispatcher, self).__init__(conf)

        LOG.info("Starting new dispatcher (%s)" % self)

        missing_cfg = set()
        for required_cfg in ('zenoss_device', 'amqp_hostname', 'amqp_port',
                             'amqp_userid', 'amqp_password',
                             'amqp_virtual_host'):

            if getattr(self.conf.dispatcher_zenoss, required_cfg, None) is None:
                missing_cfg.add(required_cfg)

        if len(missing_cfg):
            LOG.error("Zenoss dispatcher disabled due to missing required configuration: %s" %
                      (", ".join(missing_cfg)))
            self.disable_permanently()
            return

        self.reenable()

        # Create the connection pool.
        try:
            with _pool_create_sem:
                # Just in case, make sure only one thread tries to create the
                # connection pool for this dispatcher.
                if not ZenossDispatcher.pool:
                    ZenossDispatcher.pool = AMQPPool(self.conf.dispatcher_zenoss)

                # Start heartbeat thread
                if not ZenossDispatcher.heartbeat:
                    ZenossDispatcher.heartbeat = Heartbeat(self.conf.dispatcher_zenoss)
                    ZenossDispatcher.heartbeat.start()

        except Exception, e:
            LOG.error("Exception during initialization: %s" % e)
            raise e


    @property
    def enabled(self):
        if self.disable_until is None:
            return True
        else:
            if self.disable_until < datetime.datetime.now():
                self.reenable()
                return True
            return False

    def disable_for(self, seconds):
        LOG.info("Disabling %s for %d seconds", self, seconds)
        self.disable_until = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    def disable_permanently(self):
        LOG.info("Disabling %s", self)
        self.disable_until = datetime.datetime.max

    def reenable(self):
        LOG.info("Reenabling %s", self)
        self.disable_until = None

    def publish(self, amqp, routing_key, data):
        def errback(exc, interval):
            LOG.warning("Couldn't publish message: %r. Retry in %ds" % (exc, interval))

        conf = self.conf.dispatcher_zenoss

        publish_with_retry = amqp.connection.ensure(
            amqp.producer,
            amqp.producer.publish,
            errback=errback,
            max_retries=conf.amqp_max_retries,
            interval_start=conf.amqp_retry_interval_start,
            interval_step=conf.amqp_retry_interval_step,
            interval_max=conf.amqp_retry_interval_max,
            )

        publish_with_retry(data,
                           serializer='json',
                           routing_key=routing_key)

    def record_metering_data(self, data):
        conf = self.conf.dispatcher_zenoss

        if not self.enabled:
            return

        if not isinstance(data, list):
            data = [data]

        with self.pool.item() as amqp:
            if not self.enabled:
                return

            if amqp.needs_reconnect:
                amqp.reconnect()
                if amqp.needs_reconnect:
                    LOG.error("Unable to establish AMQP connection, unable to record metering data at this time. "
                              "Check AMQP connectivity and authentication credentials")
                    self.disable_for(conf.amqp_error_disable)
                    return

            for data_item in data:
                routing_key = ".".join([
                    'zenoss',
                    'openstack',
                    conf.zenoss_device,
                    'meter',
                    data_item['counter_name'],
                    data_item['resource_id']
                ])

                LOG.debug("Publishing message to %s" % (routing_key))

                self.publish(amqp, routing_key, {
                    'device': conf.zenoss_device,
                    'type': 'meter',
                    'data': data_item
                })

    def record_events(self, events):
        conf = self.conf.dispatcher_zenoss

        if not self.enabled:
            return

        LOG.info("record_events called (events=%s)" % events)

        if not isinstance(events, list):
            events = [events]

        with self.pool.item() as amqp:
            if not self.enabled:
                return

            if amqp.needs_reconnect:
                amqp.reconnect()
                if amqp.needs_reconnect:
                    LOG.error("Unable to establish AMQP connection, unable to record event data at this time. "
                              "Check AMQP connectivity and authentication credentials")
                    self.disable_for(conf.amqp_error_disable)
                    return

            for event in events:
                routing_key = ".".join([
                    'zenoss',
                    'openstack',
                    conf.zenoss_device,
                    'event',
                    event['event_type']
                ])

                LOG.debug("Publishing message to %s" % (routing_key))

                self.publish(amqp, routing_key, {
                    'device': conf.zenoss_device,
                    'type': 'event',
                    'data': event
                })

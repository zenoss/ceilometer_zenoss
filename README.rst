ceilometer_zenoss
=================

This Ceilometer dispatcher plugin ships raw event and metering data from
ceilometer to Zenoss for storage in the Zenoss event and performance databases.

This integration is done by publishing messages to Zenoss's RabbitMQ server.

A zenoss-specific event_definitions.yaml file is included.  This is the same
as the stock ceilometer one, with some additional traits added to the compute
notification events.

This dispatcher should be installed on all nodes running any ceilometer, but
particularly those running ceilometer-collector or ceilometer-agent-notification.

Installation
------------

To install the latest stable version
 * sudo pip -q install --force-reinstall https://github.com/zenoss/ceilometer_zenoss/archive/master.zip
 * sudo cp /usr/lib/python2.6/site-packages/ceilometer_zenoss/event_definitions.yaml /etc/ceilometer/


Configuration
-------------

Several changes are required in /etc/ceilometer/ceilometer.conf.

In the [DEFAULT] section, add the line:::

    dispatcher=zenoss

Place this after any other dispatchers you may already be using, such as "database",
which stores data in the ceilometer database.   If you are only using ceilometer to
feed zenoss, you do not need any other dispatchers enabled.

Add a section to the file to configure the zenoss dispatcher::
    
    [dispatcher_zenoss]
  
    # Device name that this openstack region is registered as in the zenoss UI
    zenoss_device = <device name>
    
    # Zenoss AMQP Server
    amqp_hostname = <zenoss hostname>
    amqp_port = 5672
    amqp_userid = <zenoss amqp userid>
    amqp_password = <zenoss amqp password>
    amqp_virtual_host = <zenoss amqp virtual host>

For more details on configuring these properly, consult the documentation for
the OpenstackInfrastructure ZenPack.



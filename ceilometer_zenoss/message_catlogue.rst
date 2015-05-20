========================================
Neutron Messaging
========================================

* Create Messages
* Update Messages
* Delete Messages

All these events send valid JSON messages via AMQP to Zenoss.
These events are full updates to the attributes.

Event Messages Types
================================================================================
These events have these event types:

Top Level Types
--------------------------------------------------------------------------------

* dhcp_agent.network.* [create, delete]
* firewall.*
* firewall_policy.*
* firewall_rule.*
* floatingip.*
* network.*
* port.*
* router.*
* router.interface.*
* security_group.*
* security_group_rule.*
* subnet.*

References:

   * neutron/api/v2/attributes.py
   * http://developer.openstack.org/api-ref-networking-v2.html

Secondary Event Types: Controller
--------------------------------------------------------------------------------
Reference: neutron/api/v2/base.py

* list
* show
* create
* update
* delete

Temporal Type
--------------------------------------------------------------------------------

* start
* end


Create Events
----------------------
Data from AMQP gets fed into Zenoss and cached in OSI:

EventsAMQPDataSource.processMessage::

      cache[device_id].add(value['data'], timestamp)

It is then iterated over (Collections) in same::

      for entry in cache[device_id].get():

network.create.start::

      {u'network': {
                    u'admin_state_up': True,
                    u'name': u'hello_net',
                    u'provider:network_type': u'gre',
                    u'provider:segmentation_id': 23424,
                    u'router:external': False,
                    u'shared': False,
                    u'tenant_id': u'0f7b5d96594b4446833ebaa12167ae0f'
                    }}


network.create.end (payload)::

      {'network': {
                  'admin_state_up': True,
                  'id': '171cddd3-6653-4507-bccf-9ad4dff5c7e0',
                  'name': u'xxx',
                  'provider:network_type': u'gre',
                  'provider:physical_network': None,
                  'provider:segmentation_id': 1L,
                  'router:external': False,
                  'shared': False,
                  'status': 'ACTIVE',
                  'subnets': [],
                  'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'}}

network.create.end::

   {
      "device": "warehouse.osi",
      "data": {
         "traits": [
               {
                  "dtype": 1,
                  "name": "tenant_id",
                  "value": "dbb36d51377 54461a26b970bdf8ac780"
               },
               {
                  "dtype": 1,
                  "name": "service",
                  "value": "network.warehouse.example.com"
               },
               {
                  "dtype": 1,
                  "name": "request_id",
                  "value": "req-a1411f71-518d-4a28-b1f7-9ebd2def83c4"
               }
         ],
         "generated": "2015-01-28T 19:51:57.191120",
         "event_type": "network.create.start",
         "message_id": "017e7a06-298a-4a39-9a12-28cf8708d8ad"
      },
      "type": "event"
   }

Update Events
--------------------

event_type 'subnet.create.start'::

      Pdb) pp(payload)
      {u'subnet': {u'cidr': u'12.15.15.0/24',
                   u'enable_dhcp': True,
                   u'gateway_ip': None,
                   u'ip_version': 4,
                   u'name': u'bbbxx',
                   u'network_id': u'10a893c1-01a6-438a-b231-3d5102cbc639',
                   u'tenant_id': u'0f7b5d96594b4446833ebaa12167ae0f'}}

(Pdb) event_type 'subnet.update.start'::

      (Pdb) pp(payload)
      {'id': u'4cd009f8-a8e3-495e-b308-1a15698da1a5',
       u'subnet': {u'dns_nameservers': [],
                   u'enable_dhcp': True,
                   u'host_routes': [],
                   u'name': u'bbbxxyy'}}

subnet.update.start::

      {
          "device": "warehouse.osi",
          "data": {
              "traits": [
                  {
                      "dtype": 1,
                      "name": "tenant_id",
                      "value": "dbb36d5137754461a26b970bdf8ac780"
                  },
                  {
                      "dtype": 1,
                      "name": "service",
                      "value": "network.warehouse.example.com"
                  },
                  {
                      "dtype": 1,
                      "name": "request_id",
                      "value": "req-8e5c2935-81d6-4d45-87d4-419a1174f194"
                  }
              ],
              "generated": "2015-01-28T19:41:36.713319",
              "event_type": "subnet.update.start",
              "message_id": "251a6a26-9bbf-45f4-b4f8-4015faee5f8c"
          },
          "type": "event"
      }


event_type": "subnet.update.end"::

      {
          "device": "warehouse.osi",
          "data": {
              "traits": [
                  {
                      "dtype": 1,
                      "name": "tenant_id",
                      "value": "dbb36d5137754461a26b970bdf8ac780"
                  },
                  {
                      "dtype": 1,
                      "name": "service",
                      "value": "network.warehouse.example.com"
                  },
                  {
                      "dtype": 1,
                      "name": "request_id",
                      "value": "req-13d36cc6-9139-4b4c-b5bc-8c1729fdf49a"
                  }
              ],
              "generated": "2015-01-28T17:06:45.127235",
              "event_type": "subnet.update.end",
              "message_id": "7e9e1d4c-07c0-4387-95cf-9b74c908be00"
          },
          "type": "event"
      }


network.update.start::

      {
          "device": "warehouse.osi",
          "data": {
              "traits": [
                  {
                      "dtype": 1,
                      "name": "tenant_id",
                      "value": "dbb36d5137754461a26b970bdf8ac780"
                  },
                  {
                      "dtype": 1,
                      "name": "service",
                      "value": "network.warehouse.example.com"
                  },
                  {
                      "dtype": 1,
                      "name": "request_id",
                      "value": "req-4e8eff89-a654-4032-993b-3b7be4c90e0a"
                  }
              ],
              "generated": "2015-01-28T20:07:28.363912",
              "event_type": "network.update.start",
              "message_id": "42c5aaea-a314-47d7-a124-2ba8f8946ed2"
          },
          "type": "event"
      }

network.update.end::

      {
         "device": "warehouse.osi",
         "data": {
            "traits": [
                  {
                     "dtype": 1,
                     "name": "tenant_id",
                     "value": "dbb36d5137754461a26b970bdf8ac780"
                  },
                  {
                     "dtype": 1,
                     "name": "service",
                     "value": "network.warehouse.example.com"
                  },
                  {
                     "dtype": 1,
                     "name": "request_id",
                     "value": "req-4e8eff89-a654-4032-993b-3b7be4c90e0a"
                  }
            ],
            "generated": "2015-01-28T20:07:31.928861",
            "event_type": "network.update.end",
            "message_id": "7b43828e-a421-4706-a246-d23fe38cfbd1"
         },
         "type": "event"
      }

Delete Events
----------------------

network.delete.start::

      {
         "device": "warehouse.osi",
         "data": {
            "traits": [
                  {
                     "dtype": 1,
                     "name": "tenant_id",
                     "value": "dbb36d5137754461a26b970bdf8ac780"
                  },
                  {
                     "dtype": 1,
                     "name": "service",
                     "value": "network.warehouse.example.com"
                  },
                  {
                     "dtype": 1,
                     "name": "request_id",
                     "value": "req-07dbf89a-f0c8-4497-b3f2-09d3907d33e5"
                  }
            ],
            "generated": "2015-01-28T20:24:39.413874",
            "event_type": "network.delete.start",
            "message_id": "beda74d1-9f9b-48ca-9dc7-46fc8c173205"
         },
         "type": "event"
      }


network.delete.end::

      payload: {'network_id': u'acb6ea67-4ee2-4d11-b3be-b90ce7232c4b'}

      {
         "device": "warehouse.osi",
         "data": {
            "traits": [
                  {
                     "dtype": 1,
                     "name": "tenant_id",
                     "value": "dbb36d5137754461a26b970bdf8ac780"
                  },
                  {
                     "dtype": 1,
                     "name": "service",
                     "value": "network.warehouse.example.com"
                  },
                  {
                     "dtype": 1,
                     "name": "request_id",
                     "value": "req-07dbf89a-f0c8-4497-b3f2-09d3907d33e5"
                  }
            ],
            "generated": "2015-01-28T20:25:44.247494",
            "event_type": "network.delete.end",
            "message_id": "1a1ecf36-fe12-4027-880d-20de86b9f25b"
         },
         "type": "event"
      }

Network Events: Payload
--------------------------------------------------------------------------------

network.update.end::

      {'network': {
                  'admin_state_up': True,
                  'id': u'55820ca7-2484-4d90-a2bb-b670ac329b6b',
                  'name': u'network_C9x',
                  'provider:network_type': u'gre',
                  'provider:physical_network': None,
                  'provider:segmentation_id': 9L,
                  'router:external': False,
                  'shared': False,
                  'status': u'ACTIVE',
                  'subnets': [u'ef497a89-9a03-4cd7-b6ad-ce5a6fd82439'],
                  'tenant_id': u'c9726957929e4a1ba3971954db23d240'
                  }}

network.delete.end::

      {'network_id': u'7c2cd853-51a6-446a-8ec9-c8755e02faed'}

Router Events: Payload
--------------------------------------------------------------------------------

Router event payloads on end::

router.update.start::

      {'id': u'70e4150e-cc15-47fd-a777-5157ed769db4',
       u'router':
          {u'external_gateway_info':
              {u'network_id': u'dce9ac6a-e9e2-436b-93bf-031600ef1339'}}}

router.update.end (payload)::

      {'router': {
                  'admin_state_up': True,
                  'distributed': False,
                  'external_gateway_info':
                      {'enable_snat': True,
                       'network_id': u'acb6ea67-4ee2-4d11-b3be-b90ce7232c4b',
                       'external_fixed_ips':
                           [{'ip_address': u'192.168.1.233',
                             'subnet_id': u'ab823a7a-9f06-40b9-a620-1e6591c3ee87'}]
                      },
                  'ha': False,
                  'id': u'd1e2602e-8fe3-432e-972a-c1acd799caa6',
                  'name': u'router_to_heave',
                  'routes': [],
                  'status': u'ACTIVE',
                  'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'
                  }}


router.interface.create::

      {'router_interface':
           {
           'id': u'ad89936d-3d2f-4c63-942c-920760c994bb',
           'port_id': '4688d778-0a6f-4883-b393-eee54bab95d1',
           'subnet_id': u'd3c18d0a-4876-4420-9020-824be2684156',
           'tenant_id': u'f873d72ccd7744bfa8355c8833f203a2'
           }}

router.interface.delete::

      (Pdb) pprint.pprint(payload)
      {'router_interface':
          {'id': u'ed783e7d-8928-47ac-ac13-1736510703fe',
           'port_id': u'35324357-cc1e-4e79-bebb-790ad801ed7f',
           'subnet_id': u'0e8642f2-142f-453f-9f7e-357e8074142d',
           'tenant_id': u'1bfee2f15d8e4c9596192a1a9dee4c20'}}


router.create.start::

      {u'router': {u'admin_state_up': True,
                   u'name': u'router_AB',
                   u'tenant_id': u'0f7b5d96594b4446833ebaa12167ae0f'}}

router.create.end::

      {'router': {
            'admin_state_up': True,
            'distributed': False,
            'external_gateway_info': None,
            'ha': False,
            'id': 'ad89936d-3d2f-4c63-942c-920760c994bb',
            'name': u'router_AB',
            'routes': [],
            'status': 'ACTIVE',
            'tenant_id': u'0f7b5d96594b4446833ebaa12167ae0f'
            }}

router.delete.end::

      {'router_id': u'ed783e7d-8928-47ac-ac13-1736510703fe'}


router.update.end (json)::

      {
      "device": "warehouse.osi",
      "data": {
         "traits": [
            {
            "dtype": 1,
            "name": "external_gateway_info",
            "value": "{u'network_id': u'10a893c1-01a6-438a-b231-3d5102cbc639', u'enable_snat': True, u'external_fixed_ips': [{u'subnet_id': u'f2d8864a-0efb-4667-9194-7a6e3b9a7bb2', u'ip_address': u'192.168.1.226'}]}"
            },
            {
            "dtype": 1,
            "name": "status",
            "value": "ACTIVE"
            },
            {
            "dtype": 1,
            "name": "event_type",
            "value": "router.update.end"
            },
            {
            "dtype": 1,
            "name": "service",
            "value": "network.warehouse.example.com"
            },
            {
            "dtype": 1,
            "name": "admin_state_up",
            "value": "False"
            },
            {
            "dtype": 1,
            "name": "tenant_id",
            "value": "49adcfb63f4640038498be2bd417614e"
            },
            {
            "dtype": 1,
            "name": "distributed",
            "value": "False"
            },
            {
            "dtype": 1,
            "name": "priority",
            "value": "info"
            },
            {
            "dtype": 1,
            "name": "request_id",
            "value": "req-a491923d-92b9-4982-b1e4-04db848bad49"
            },
            {
            "dtype": 1,
            "name": "routes",
            "value": "[]"
            },
            {
            "dtype": 1,
            "name": "ha",
            "value": "False"
            },
            {
            "dtype": 1,
            "name": "id",
            "value": "376cea18-32c1-43f7-bbd5-5201bc322812"
            },
            {
            "dtype": 1,
            "name": "name",
            "value": "router_C"
            }
         ],
         "generated": "2015-02-27T19:58:54.532868",
         "event_type": "router.update.end",
         "message_id": "1c176b65-c887-4a3c-b2aa-31336eb51528"
      },
      "type": "event"
      }

Port Events: Payload
--------------------------------------------------------------------------------

port.delete.end::

      {'port_id': u'e584ce52-f7e1-4884-9801-f3cde90f32e3'}

port.create.start::

      {u'port': {
                 u'admin_state_up': True,
                 u'binding:host_id': u'warehouse.example.com',
                 u'device_id': u'23863c1e-2dff-4c96-9ba4-13d07f1f4abf',
                 u'device_owner': u'compute:None',
                 u'network_id': u'dce9ac6a-e9e2-436b-93bf-031600ef1339',
                 u'security_groups': [u'a6e24018-58e3-4f4c-a8e0-cfc47b15730c'],
                 u'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'
                 }}

port.create.end::

      (Pdb) pprint.pprint(payload)
      {'port': {
               'admin_state_up': True,
               'allowed_address_pairs': [],
               'binding:host_id': u'warehouse.example.com',
               'binding:profile': {},
               'binding:vif_details': {u'ovs_hybrid_plug': True, u'port_filter': True},
               'binding:vif_type': u'ovs',
               'binding:vnic_type': u'normal',
               'device_id': u'd1e2602e-8fe3-432e-972a-c1acd799caa6',
               'device_owner': u'network:router_gateway',
               'extra_dhcp_opts': [],
               'fixed_ips': [{'ip_address': u'192.168.1.233', 'subnet_id': u'ab823a7a-9f06-40b9-a620-1e6591c3ee87'}],
               'id': u'c79bacd3-2659-49d6-97fb-299cfa3dc7a3',
               'mac_address': u'fa:16:3e:32:f6:fa',
               'name': u'bozo_port',
               'network_id': u'acb6ea67-4ee2-4d11-b3be-b90ce7232c4b',
               'security_groups': [],
               'status': u'DOWN',
               'tenant_id': u''
               }}

Subnet Events: Payload
--------------------------------------------------------------------------------

Subnet events::

      (Pdb) event_type
      'subnet.create.start'
      (Pdb) pprint.pprint(payload)
      {u'subnet': {
                  u'cidr': u'10.20.50.0/24',
                  u'enable_dhcp': True,
                  u'gateway_ip': u'10.20.50.1',
                  u'ip_version': 4,
                  u'name': u'xxx_subnet',
                  u'network_id': u'6b7fb9d3-2c36-4d3c-848a-46ed6d1c37ff'}}


      (Pdb) event_type
subnet.create.end::

      # Address as payload.subnet.*

      (Pdb) result
      {'subnet':
         {
          'allocation_pools': [{'start': '10.10.10.2', 'end': '10.10.10.254'}],
          'cidr': '10.10.10.0/24',
          'dns_nameservers': [],
          'enable_dhcp': True,
          'gateway_ip': '10.10.10.1',
          'host_routes': [],
          'id': '27bad7ac-780f-4d90-aa7d-a4406eace55c'}
          'ipv6_address_mode': None,
          'ipv6_ra_mode': None,
          'ip_version': 4L,
          'name': 'bbbxxYY',
          'network_id': '6e15368b-e2e4-4488-b282-efa8a3af016b',
          'tenant_id': 'dbb36d5137754461a26b970bdf8ac780',
       }

subnet.delete.end::

       (Pdb) pprint.pprint(payload)
       {'subnet_id': u'55f53c72-1983-4793-a5f7-c1775699da4a'}

 Security Events
--------------------------------------------------------------------------------

security_group.delete.end::

      {'security_group_id': u'460cd81e-d918-46f7-877e-0c261efc870d'}

security_group.create.end::

      {'security_group':
            {'description': u'test sg',
             'id': u'460cd81e-d918-46f7-877e-0c261efc870d',
             'name': u'sg_nobodya',
             'security_group_rules':
                  [{'direction': u'egress',
                    'ethertype': u'IPv4',
                    'id': u'a7e54ea9-9eeb-4689-9107-b9367f8ae229',
                    'port_range_max': None,
                    'port_range_min': None,
                    'protocol': None,
                    'remote_group_id': None,
                    'remote_ip_prefix': None,
                    'security_group_id': u'460cd81e-d918-46f7-877e-0c261efc870d',
                    'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'},
                   {'direction': u'egress',
                    'ethertype': u'IPv6',
                    'id': u'aa6c749a-b9ae-4f19-ae2a-7e7e19c9312f',
                    'port_range_max': None,
                    'port_range_min': None,
                    'protocol': None,
                    'remote_group_id': None,
                    'remote_ip_prefix': None,
                    'security_group_id': u'460cd81e-d918-46f7-877e-0c261efc870d',
                    'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'}],
              'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'
            }}

security_group_rule::

    (Pdb) pprint.pprint(payload)
    {'security_group_rule':
        {
         'direction': u'ingress',
         'ethertype': 'IPv4',
         'id': '72ed47e0-6975-4e8c-a3ce-1a0ac20862b8',
         'port_range_max': 53,
         'port_range_min': 53,
         'protocol': u'tcp',
         'remote_group_id': None,
         'remote_ip_prefix': '0.0.0.0/0',
         'security_group_id': u'460cd81e-d918-46f7-877e-0c261efc870d',
         'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'
         }}

IP Events
===============================================================================

FloatingIP Events
--------------------------------------------------------------------------------
FloatingIP Events look like::

floatingip.create.start::

    {u'floatingip': {
                     u'fixed_ip_address': u'10.1.7.100',
                     u'floating_network_id': u'1fb467ad-a996-4520-b941-27962e152a7e',
                     u'port_id': u'edd51762-9bd9-498a-a1ae-6ff7941622c9'
                     }}

floatingip.create.end::

    (Pdb) pprint.pprint(payload)
    {'floatingip': {
                'fixed_ip_address': u'10.1.7.100',
                'floating_ip_address': u'192.168.1.229',
                'floating_network_id': u'1fb467ad-a996-4520-b941-27962e152a7e',
                'id': 'd605daeb-4353-4250-8d72-76a702b6d75f',
                'port_id': u'edd51762-9bd9-498a-a1ae-6ff7941622c9',
                'router_id': u'c28211ba-2d78-4aef-91a7-6339cf6b97bc',
                'status': 'DOWN',
                'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'}}

floatingip.delete.start::

    (Pdb) event_type ; payload
    {'floatingip_id': u'9330d094-4c50-4023-a8fd-83f7e0dd0826'}

floatingip.delete.end::

    payload:
    {'floatingip_id': u'87b250d7-ffeb-4ebf-a164-501ccb5e9af5'}


FloatingIP Association Events
--------------------------------------------------------------------------------
FloatingIP Association Events look like::


DHCP_AGENT Events
--------------------------------------------------------------------------------
DHCP_AGENT Events look like::

dhcp_agent.network.add::

   {'agent': {'id': u'81c61c6a-8728-44c3-a779-5376182cb960',
            'network_id': u'acb6ea67-4ee2-4d11-b3be-b90ce7232c4b'}}

dhcp_agent.network.remove::

   {'agent': {'id': u'81c61c6a-8728-44c3-a779-5376182cb960',
            'network_id': u'acb6ea67-4ee2-4d11-b3be-b90ce7232c4b'}}

   # Json output via AMQP
   {
    "device": "warehouse.osi",
    "data": {
        "traits": [
            {
                "dtype": 1,
                "name": "priority",
                "value": "info"
            },
            {
                "dtype": 1,
                "name": "tenant_id",
                "value": "dbb36d5137754461a26b970bdf8ac780"
            },
            {
                "dtype": 1,
                "name": "payload",
                "value": "{u'agent': {u'network_id': u'acb6ea67-4ee2-4d11-b3be-b90ce7232c4b', u'id': u'81c61c6a-8728-44c3-a779-5376182cb960'}}"
            },
            {
                "dtype": 1,
                "name": "service",
                "value": "network.warehouse.example.com"
            },
            {
                "dtype": 1,
                "name": "request_id",
                "value": "req-20ad5550-9a58-43fa-bc7e-47b981fef2e9"
            }
        ],
        "generated": "2015-01-30T23:21:45.341349",
        "event_type": "dhcp_agent.network.remove",
        "message_id": "377e66bf-3137-47b2-aae1-89e95fe443c3"
    },
    "type": "event"
}

Reporting Events
=====================

meter::

   {
       "device": "warehouse.osi",
       "data": {
           "counter_name": "storage.objects",
           "user_id": null,
           "message_signature": "14f5a9d69f986873513fa5e48b003a73cb317cff90239f858e9998594fd78bf4",
           "timestamp": "2015-01-28T20:55:44.000000",
           "resource_id": "f873d72ccd7744bfa8355c8833f203a2",
           "message_id": "06d465c0-a730-11e4-a546-6ee7bc346542",
           "source": "openstack",
           "counter_unit": "object",
           "counter_volume": 0,
           "project_id": "f873d72ccd7744bfa8355c8833f203a2",
           "resource_metadata": null,
           "counter_type": "gauge"
       },
       "type": "meter"
   }

   {
      "device": "warehouse.osi",
      "data": {
         "counter_name": "image.size",
         "user_id": null,
         "message_signature": "bd54edafe0209814d0402f81844831cbbeef332763d1d5b16430db1a9b28abb1",
         "timestamp": "2015-01-28T20:55:44.000000",
         "resource_id": "d764b678-ad50-431a-84a5-219be3ebf17e",
         "message_id": "06f9007e-a730-11e4-a546-6ee7bc346542",
         "source": "openstack",
         "counter_unit": "B",
         "counter_volume": 13200896,
         "project_id": "None",
         "resource_metadata": {
               "status": "active",
               "name": "cirros",
               "deleted": false,
               "container_format": "bare",
               "created_at": "2015-01-05T14:22:52",
               "disk_format": "qcow2",
               "updated_at": "2015-01-05T14:22:54",
               "properties": {

               },
               "protected": false,
               "checksum": "133eae9fb1c98f45894a4e60d8736619",
               "min_disk": 0,
               "is_public": true,
               "deleted_at": null,
               "min_ram": 0,
               "size": 13200896
         },
         "counter_type": "gauge"
      },
      "type": "meter"
   }


Firewall Events
===================


firewall_rule.create.end, firewall_rule.update.end::

      (Pdb) pprint.pprint(payload)
      {'firewall_rule': {
               'action': u'allow',
               'description': '',
               'destination_ip_address': None,
               'destination_port': '80',
               'enabled': True,
               'firewall_policy_id': None,
               'id': '629d9c7e-5421-40b1-9ae5-fc92e50c8794',
               'ip_version': 4,
               'name': '',
               'position': None,
               'protocol': u'tcp',
               'shared': False,
               'source_ip_address': None,
               'source_port': None,
               'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'}}


firewall_rule.delete.end::

      {'firewall_rule_id': u'6e257aee-f881-4db5-ae95-48a78e0cd519'}

firewall_policy.create.end::
firewall_policy.update.end::

      {'firewall_policy':
          {
            'audited': False,
            'description': '',
            'firewall_rules': [u'6e257aee-f881-4db5-ae95-48a78e0cd519', u'7661788c-20b1-4e42-afab-b3479d18afff'],
            'id': 'd598932e-e0ef-4f5d-bd4c-ce1abb40ba26',
            'name': u'web',
            'shared': False,
            'tenant_id': u'dbb36d5137754461a26b970bdf8ac780' }}

firewall_policy.delete.end::

      {'firewall_policy_id': u'd598932e-e0ef-4f5d-bd4c-ce1abb40ba26'}

firewall.create.end::
firewall.update.end::

      {'firewall': {
          'admin_state_up': True,
          'description': '',
          'firewall_policy_id': u'd598932e-e0ef-4f5d-bd4c-ce1abb40ba26',
          'id': '76a9e5c0-07dd-4106-bd96-18f3420f534b',
          'name': '',
          'status': 'PENDING_CREATE',
          'tenant_id': u'dbb36d5137754461a26b970bdf8ac780'}}

firewall.delete.end::

      {'firewall_id': u'76a9e5c0-07dd-4106-bd96-18f3420f534b'}


Keystone Events:
-----------------------------------------------------------------------------

(Pdb) event_type
'identity.project.deleted'::

   (Pdb) pp(payload)
   {'resource_info': u'4220802f7daf41e98b912fa99e51ac82'}

(Pdb) event_type
'identity.project.created'::

   (Pdb) pp(payload)
   {'resource_info': '9fc63b96892b4e47a330946b355d7913'}


event_type: 'identity.user.created'::

    payload: {'resource_info': '340df92410db4629a75030eeed3aba6b'}

event_type: 'identity.user.updated'::

    payload: {'resource_info': u'340df92410db4629a75030eeed3aba6b'}

event_type: 'identity.user.updated'::

    payload: {'resource_info': u'340df92410db4629a75030eeed3aba6b'}


Instance Events
-------------------------------------------------------------------------------

compute.instance.update::

   {
   "traits": [
      {
         "dtype": 1,
         "name": "state_description",
         "value": ""
      },
      {
         "dtype": 2,
         "name": "memory_mb",
         "value": 64
      },
      {
         "dtype": 2,
         "name": "ephemeral_gb",
         "value": 0
      },
      {
         "dtype": 1,
         "name": "user_id",
         "value": "fb45e55b12754390ac530341256cab60"
      },
      {
         "dtype": 1,
         "name": "service",
         "value": "None"
      },
      {
         "dtype": 1,
         "name": "priority",
         "value": "info"
      },
      {
         "dtype": 1,
         "name": "state",
         "value": "active"
      },
      {
         "dtype": 1,
         "name": "old_state",
         "value": "active"
      },
      {
         "dtype": 4,
         "name": "launched_at",
         "value": "2015-04-17T22:15:24.000000"
      },
      {
         "dtype": 1,
         "name": "flavor_name",
         "value": "tiny"
      },
      {
         "dtype": 2,
         "name": "disk_gb",
         "value": 0
      },
      {
         "dtype": 1,
         "name": "display_name",
         "value": "bogus122"
      },
      {
         "dtype": 2,
         "name": "root_gb",
         "value": 0
      },
      {
         "dtype": 1,
         "name": "tenant_id",
         "value": "dbb36d5137754461a26b970bdf8ac780"
      },
      {
         "dtype": 1,
         "name": "instance_id",
         "value": "d9c87692-9590-4313-b97a-132d1cc6b51a"
      },
      {
         "dtype": 2,
         "name": "vcpus",
         "value": 1
      },
      {
         "dtype": 1,
         "name": "host_name",
         "value": "warehouse.example.com"
      },
      {
         "dtype": 1,
         "name": "request_id",
         "value": "req-ff00f04c-e1f7-4acb-97d2-f0bd40bda411"
      }
   ],
   "generated": "2015-04-22T17:46:53.428072",
   "event_type": "compute.instance.update",
   "message_id": "5e0bcd5d-1b64-4997-b293-700fe6b6fa1a"
   }


"event_type": "compute.instance.create.end"::

   {
   "device": "warehouse.osi",
   "data": {
      "traits": [
         {
         "dtype": 1,
         "name": "state_description",
         "value": ""
         },
         {
         "dtype": 2,
         "name": "memory_mb",
         "value": 64
         },
         {
         "dtype": 2,
         "name": "ephemeral_gb",
         "value": 0
         },
         {
         "dtype": 1,
         "name": "fixed_ips",
         "value": "[{u'version': 4,
                     u'vif_mac': u'fa:16:3e:35:99:b1',
                     u'floating_ips': [],
                     u'label': u'network_public',
                     u'meta': {},
                     u'address': u'10.1.2.13',
                     u'type': u'fixed'}]"
         },
         {
         "dtype": 1,
         "name": "user_id",
         "value": "fb45e55b12754390ac530341256cab60"
         },
         {
         "dtype": 1,
         "name": "service",
         "value": "compute"
         },
         {
         "dtype": 1,
         "name": "priority",
         "value": "info"
         },
         {
         "dtype": 1,
         "name": "state",
         "value": "active"
         },
         {
         "dtype": 4,
         "name": "launched_at",
         "value": "2015-04-22T18:12:33.447644"
         },
         {
         "dtype": 1,
         "name": "flavor_name",
         "value": "tiny"
         },
         {
         "dtype": 2,
         "name": "disk_gb",
         "value": 0
         },
         {
         "dtype": 1,
         "name": "display_name",
         "value": "bogus"
         },
         {
         "dtype": 2,
         "name": "root_gb",
         "value": 0
         },
         {
         "dtype": 1,
         "name": "tenant_id",
         "value": "dbb36d5137754461a26b970bdf8ac780"
         },
         {
         "dtype": 1,
         "name": "instance_id",
         "value": "3b5ea38c-51fd-43f4-a9f7-7b876e9561e4"
         },
         {
         "dtype": 2,
         "name": "vcpus",
         "value": 1
         },
         {
         "dtype": 1,
         "name": "host_name",
         "value": "warehouse.example.com"
         },
         {
         "dtype": 1,
         "name": "request_id",
         "value": "req-184c803c-bf92-46f9-9aeb-fac007d4e049"
         }
      ],
      "generated": "2015-04-22T18:12:34.202399",
      "event_type": "compute.instance.create.end",
      "message_id": "80fbf56b-b3d4-40c9-968e-f6e4ee8042c8"
   },
   "type": "event"
   }

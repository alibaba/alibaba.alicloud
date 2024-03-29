#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. <xiaozhu36>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_route_entry_info
short_description: Gather facts on vrouter of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the VRouter itself.
options:    
    vrouter_id:
      description:
        - Id of vrouter of vpc
      aliases: ["id"]
      type: str
    route_table_id:
     description:
        - The ID of the route table.
     type: str
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alibaba.alicloud.alicloud
'''

EXAMPLES = '''
# Fetch vrouter details according to setting different filters
- name: Find all vroute_entries in the specified vroute
  alibaba.alicloud.ali_route_entry_info:
    vrouter_id: '{{ vrouter_id }}'
    
- name: Find all vroute_entries in the specified vroute by route table id
  alibaba.alicloud.ali_route_entry_info:
    vrouter_id: '{{ vrouter_id }}'
    route_table_id: '{{ route_table_id }}'  

'''

RETURN = '''
vrouter_id:
    description: VRouter id after operating VRouter.
    returned: when success
    type: str
    sample: "vrt-2ze60agfbr2wcyt08jfov"
vroute_entries:
    description: Details about the VRouter that were created.
    returned: when success
    type: list
    sample: [
        {
            "destination_cidr_block": "192.168.5.0/28",
            "instance_id": "",
            "next_hop_type": "local",
            "next_hops": {
                "next_hop": []
            },
            "region": "cn-beijing",
            "route_table_id": "vtb-2ze1rxml89cl7828yc08g",
            "status": "Available",
            "tags": {},
            "type": "System"
        },
        {
            "destination_cidr_block": "192.168.1.0/24",
            "instance_id": "",
            "next_hop_type": "local",
            "next_hops": {
                "next_hop": []
            },
            "region": "cn-beijing",
            "route_table_id": "vtb-2ze1rxml89cl7828yc08g",
            "status": "Available",
            "tags": {},
            "type": "System"
        },
        {
            "destination_cidr_block": "100.64.0.0/10",
            "instance_id": "",
            "next_hop_type": "service",
            "next_hops": {
                "next_hop": []
            },
            "region": "cn-beijing",
            "route_table_id": "vtb-2ze1rxml89cl7828yc08g",
            "status": "Available",
            "tags": {},
            "type": "System"
        }
    ]
total:
    description: The number of all route entries in vrouter.
    returned: when success
    type: int
    sample: 3
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.alibaba.alicloud.plugins.module_utils.alicloud_ecs import ecs_argument_spec, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import VPCResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(route_entry):
    """
        Retrieves route entry information from an route entry
        ID and returns it as a dictionary
    """
    return {
        'destination_cidr_block': route_entry.destination_cidr_block,
        'instance_id': route_entry.instance_id,
        'next_hop_type': route_entry.next_hop_type,
        'next_hops': route_entry.next_hops,
        'region': route_entry.region,
        'route_table_id': route_entry.route_table_id,
        'status': route_entry.status,
        'tags': route_entry.tags,
        'type': route_entry.type,
        'route_entry_id': route_entry.route_entry_id,
        'route_entry_name': route_entry.route_entry_name
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        vrouter_id=dict(type='str', required=True, aliases=['id']),
        route_table_id=dict(type='str')
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    result = []
    vrouter_id = module.params['vrouter_id']
    route_table_id = module.params['route_table_id']


    try:
        vpc_conn = vpc_connect(module)

        # list all route entries in vrouter
        if vrouter_id:
            vrouter_entries = vpc_conn.get_all_route_entries(router_id=vrouter_id, route_table_id=route_table_id)
            for vrouter_entry in vrouter_entries:
                result.append(get_info(vrouter_entry))
    except Exception as e:
        module.fail_json(msg="Unable to describe vrouter entries, and got an error: {0}.".format(e))

    module.exit_json(changed=False, vrouter_id=vrouter_id,  vroute_entries=result, total=len(result))


if __name__ == '__main__':
    main()

#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
#  This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see http://www.gnu.org/licenses/.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_vswitch_facts
version_added: "2.4"
short_description: Gather facts on vswitchs of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the vswitch itself.

options:
    vpc_id:
      description:
        - A vpc id to list vswitches in specified vpc.
      required: true
      aliases: ["id"]
    vswitch_ids:
      required: false
      description:
        - A list of vswitch ids.      
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch vswitch details according to setting different filters
- name: Fetch vswitch details example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    vpc_id: xxxxxxxxxxxxx
    vswitch_ids:
      - xxxxxxxxxxxxx
      - xxxxxxxxxxxxx
  tasks:
    - name: Find all vswitches in the specified vpc
      alicloud_vswitch_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vpc_id: '{{ vpc_id }}'
      register: vswitch_by_vpc
    - debug: var=vswitch_by_vpc

    - name: Find all vswitches in the specified vpc by vswitch_ids
      alicloud_vswitch_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vpc_id: '{{ vpc_id }}'
        vswitch_ids: '{{ vswitch_ids }}'
      register: vswich_by_vswitch_ids
    - debug: var=vswich_by_vswitch_ids

'''

RETURN = '''
vpc_id:
    description: vpc_id to list all vswitch in specified vpc.
    returned: when success
    type: string
    sample: "vpc-2zegusms7jwd94lq7ix8o"
vswitch_ids:
    description: List all vswitch's id after operating vswitch.
    returned: when success
    type: list
    sample:  [ "vsw-2zepee91iv5sl6tg85xnl", "vsw-2zeuo4b8jx8tdg9esy8m7" ]
vswitchs:
    description: Details about the vswitchs that were created.
    returned: when success
    type: list
    sample: [
        {
            "available_ip_address_count": 4091,
            "cidr_block": "172.17.128.0/20",
            "description": "System created default virtual switch.",
            "is_default": true,
            "region": "cn-beijing",
            "status": "Available",
            "tags": {},
            "vpc_id": "vpc-2zegusms7jwd94lq7ix8o",
            "vswitch_id": "vsw-2zepee91iv5sl6tg85xnl",
            "vswitch_name": "",
            "zone_id": "cn-beijing-e"
        },
        {
            "available_ip_address_count": 4092,
            "cidr_block": "172.17.144.0/20",
            "description": "System created default virtual switch.",
            "is_default": true,
            "region": "cn-beijing",
            "status": "Available",
            "tags": {},
            "vpc_id": "vpc-2zegusms7jwd94lq7ix8o",
            "vswitch_id": "vsw-2zeuo4b8jx8tdg9esy8m7",
            "vswitch_name": "",
            "zone_id": "cn-beijing-c"
        }
    ]    
total:
    description: The number of all vswitchs after operating vpc.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import VPCResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(vswitch):
    """
        Retrieves vswitch information from an vswitch
        ID and returns it as a dictionary
    """
    return {
        'available_ip_address_count': vswitch.available_ip_address_count,
        'cidr_block': vswitch.cidr_block,
        'description': vswitch.description,
        'is_default': vswitch.is_default,
        'region': vswitch.region,
        'status': vswitch.status,
        'tags': vswitch.tags,
        'vpc_id': vswitch.vpc_id,
        'vswitch_id': vswitch.vswitch_id,
        'vswitch_name': vswitch.vswitch_name,
        'zone_id': vswitch.zone_id
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        alicloud_zone=dict(aliases=['acs_zone', 'ecs_zone', 'zone_id', 'zone']),
        vpc_id=dict(required=True, aliases=['id']),
        vswitch_ids=dict(type='list')
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    result = []
    zone_id = module.params['alicloud_zone']
    vpc_id = module.params['vpc_id']
    vswitch_ids = module.params['vswitch_ids']

    if vswitch_ids and (not isinstance(vswitch_ids, list) or len(vswitch_ids)) < 1:
        module.fail_json(msg='vswitch_ids should be a list of vswitch id, aborting')

    try:
        vpc_conn = vpc_connect(module)

        # list all vswitches by vswitch ids
        if vswitch_ids:
            for vswitch_id in vswitch_ids:
                vswitchs = vpc_conn.get_all_vswitches(vpc_id=vpc_id, vswitch_id=vswitch_id, zone_id=zone_id)
                if vswitchs and len(vswitchs) == 1:
                    result.append(get_info(vswitchs[0]))

        # list all vswitches in specified vpc
        else:
            vswitchs = vpc_conn.get_all_vswitches(vpc_id=vpc_id)
            vswitch_ids = []
            for vswitch in vswitchs:
                vswitch_ids.append(vswitch.vswitch_id)
                result.append(get_info(vswitch))
    except Exception as e:
        module.fail_json(msg=str("Unable to describe vswitch, error:{0}".format(e)))

    module.exit_json(changed=False, vpc_id=vpc_id, vswitch_ids=vswitch_ids, vswitchs=result, total=len(result))


if __name__ == '__main__':
    main()

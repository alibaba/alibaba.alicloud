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
module: alicloud_vpc_facts
version_added: "2.4"
short_description: Gather facts on vpcs of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the vpc itself.

options:
    vpc_ids:
      description:
        - A list of vpc ids.
      aliases: ["ids"]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch vpc details according to setting different filters
- name: Fetch vpc details example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    vpc_ids:
      - xxxxxxxxxxxxx
      - xxxxxxxxxxxxx
  tasks:
    - name: Find all vpcs in the specified region
      alicloud_vpc_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
      register: vpcs_by_region
    - debug: var=vpcs_by_region
    
    - name: Find all vpcs in the specified region by vpc_ids
      alicloud_vpc_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vpc_ids: '{{ vpc_ids }}'
      register: vpcs_by_ids
    - debug: var=vpcs_by_ids
'''

RETURN = '''
vpc_ids:
    description: List all vpc's id after operating vpc.
    returned: when success
    type: list
    sample: [ "vpc-2zegusms7jwd94lq7ix8o", "vpc-2ze5hrb3y5ksx5oa3a0xa" ]
vpcs:
    description: Details about the vpcs that were created.
    returned: when success
    type: list
    sample: [
        {
            "cidr_block": "172.17.0.0/16",
            "description": "System created default VPC.",
            "is_default": true,
            "region_id": "cn-beijing",
            "status": "Available",
            "tags": {},
            "user_cidrs": {
                "user_cidr": []
            },
            "vpc_id": "vpc-2zegusms7jwd94lq7ix8o",
            "vpc_name": "",
            "vrouter_id": "vrt-2zepnt8dmohmif634a85l",
            "vswitch_ids": {
                "vswitch_id": [
                    "vsw-2zepee91iv5sl6tg85xnl",
                    "vsw-2zeuo4b8jx8tdg9esy8m7",
                    "vsw-2ze0qexkkuocpru16yh5p"
                ]
            }
        },
        {
            "cidr_block": "192.168.0.0/16",
            "description": "",
            "is_default": false,
            "region_id": "cn-beijing",
            "status": "Available",
            "tags": {},
            "user_cidrs": {
                "user_cidr": []
            },
            "vpc_id": "vpc-2ze5hrb3y5ksx5oa3a0xa",
            "vpc_name": "dmeo_vpc",
            "vrouter_id": "vrt-2ze60agfbr2wcyt08jfov",
            "vswitch_ids": {
                "vswitch_id": [
                    "vsw-2zewmmqum64hvlrididef",
                    "vsw-2zeob1v20umn67x6i5ybx"
                ]
            }
        }
    ]    
total:
    description: The number of all vpcs after operating vpc.
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


def get_info(vpc):
    """
        Retrieves vpc information from an vpc
        ID and returns it as a dictionary
    """
    return {
        'cidr_block': vpc.cidr_block,
        'description': vpc.description,
        'is_default': vpc.is_default,
        'region_id': vpc.region_id,
        'status': vpc.status,
        'tags': vpc.tags,
        'user_cidrs': vpc.user_cidrs,
        'vpc_id': vpc.vpc_id,
        'vpc_name': vpc.vpc_name,
        'vrouter_id': vpc.vrouter_id,
        'vswitch_ids': vpc.vswitch_ids
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        vpc_ids=dict(type='list', aliases=['ids'])
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    result = []
    vpc_ids = module.params['vpc_ids']

    if vpc_ids and (not isinstance(vpc_ids, list) or len(vpc_ids)) < 1:
        module.fail_json(msg='vpc_ids should be a list of vpc id, aborting')

    try:
        vpc_conn = vpc_connect(module)

        # list all vpc's by ids
        if vpc_ids:
            for vpc_id in vpc_ids:
                vpcs = vpc_conn.get_all_vpcs(vpc_id=vpc_id)
                if vpcs and len(vpcs) == 1:
                    result.append(get_info(vpcs[0]))

        # list all vpc's in specified region
        else:
            vpcs = vpc_conn.get_all_vpcs()
            vpc_ids = []
            for vpc in vpcs:
                vpc_ids.append(vpc.vpc_id)
                result.append(get_info(vpc))
    except Exception as e:
        module.fail_json(msg=str("Unable to describe vpc, error:{0}".format(e)))

    module.exit_json(changed=False, vpc_ids=vpc_ids,  vpcs=result, total=len(result))


if __name__ == '__main__':
    main()

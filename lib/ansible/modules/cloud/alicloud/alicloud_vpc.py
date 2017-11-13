#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This file is part of Ansible
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: alicloud_vpc
version_added: "2.5"
short_description: Create, Query or Delete Vpc. Query Vswitch.
description:
    - Create, Query or Delete Vpc, and Query vswitch which in it.
options:
  state:
    description:
      -  Whether or not to create, delete or query VPC.
    choices: ['present', 'absent', 'list']
    default: 'present'
  vpc_name:
    description:
      - The name of VPC, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, "_" or "-".
        It cannot begin with http:// or https://.
    aliases: [ 'name' ]
  description:
    description:
      - The description of VPC, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
  cidr_block:
    description:
      - The CIDR block representing the vpc. The value can be subnet block of its choices. It is required when creating a vpc.
    default: '172.16.0.0/12'
    choices: ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
    aliases: [ 'cidr' ]
  user_cidr:
    description:
      - User custom cidr in the VPC. Multiple cidr should be separated by comma, and no more than three.
  vpc_id:
    description:
      - The ID of a VPC. It required when managing an existing VPC. Such as deleting vpc and querying vpc attribute.
  is_default:
    description:
      - When retrieving vpc, it can mark the VPC is created by system.
    type: bool
notes:
  - There will be launch a virtual router along with creating a vpc successfully.
  - There is only one virtual router in one vpc and one route table in one virtual router.
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"

"""

EXAMPLES = """
#
# provisioning to create vpc in VPC
#

# basic provisioning example to create vpc in VPC
- name: create vpc
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    state: present
    cidr_block: 192.168.0.0/16
    vpc_name: Demo_VPC
    description: Demo VPC
  tasks:
    - name: create vpc
      alicloud_vpc:
        alicloud_region: '{{ alicloud_region }}'
        state: '{{ state }}'
        cidr_block: '{{ cidr_block }}'
        vpc_name: '{{ vpc_name }}'
        description: '{{ description }}'
      register: result
    - debug: var=result

# basic provisioning example to delete vpc
- name: delete vpc
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
  tasks:
    - name: delete vpc
      alicloud_vpc:
        alicloud_region: '{{ alicloud_region }}'
        state: absent
        vpc_id: xxxxxxxxxx
      register: result
    - debug: var=result

"""

RETURN = '''
vpc_id:
    description: id of the vpc
    returned: on present and absent
    type: string
    sample: "vpc-2zevlzpjz2dmkj0lgxa9j"
vpc_ids:
    description: list ids of vpcs
    returned: on list
    type: list
    sample: ["vpc-2zevlzpjz2dmkj0lgxa9j", "vpc-3rvlzpjz2dmkj0lgxaxe"]
vpc:
    description: Details about the ecs vpc that was created.
    returned: on present
    type: dict
    sample: {
       "cidr_block": "10.0.0.0/8",
       "creation_time": "2017-06-20T08:07:05Z",
       "description": "travis-ansible-vpc",
       "id": "vpc-2zeqndzfcsfavl93wrwsf",
       "is_default": false,
       "name": "travis-ansible-vpc",
       "region": "cn-beijing",
       "status": "Available",
       "user_cidrs": {
           "user_cidr": []
       },
       "router_id": "vrt-2ze89k29g4zn7afavd6tc",
       "vswitch_ids": {
           "vswitch_id": []
       }
    }
vpcs:
    description: Details about the vpcs that were retrieved.
    returned: on list
    type: list
    sample: [
        {
           "cidr_block": "10.0.0.0/8",
           "creation_time": "2017-06-20T08:07:05Z",
           "description": "travis-ansible-vpc",
           "id": "vpc-2zeqndzfcsfavl93wrwsf",
           "is_default": false,
           "name": "travis-ansible-vpc",
           "region": "cn-beijing",
           "status": "Available",
           "user_cidrs": {
               "user_cidr": []
           },
           "router_id": "vrt-2ze89k29g4zn7afavd6tc",
           "vswitch_ids": {
               "vswitch_id": []
           }
        },
        {
           "cidr_block": "10.0.0.0/8",
           "creation_time": "2017-06-20T08:07:05Z",
           "description": "travis-ansible-vpc",
           "id": "vpc-2zeqndzfcsfavl93wrwsf",
           "is_default": false,
           "name": "travis-ansible-vpc",
           "region": "cn-beijing",
           "status": "Available",
           "user_cidrs": {
               "user_cidr": []
           },
           "router_id": "vrt-2ze89k29g4zn7afavd6tc",
           "vswitch_ids": {
               "vswitch_id": []
           }
        }
    ]
total:
    description: The number of all vpcs after listing vpcs.
    returned: on list
    type: int
    sample: 3
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import VPCResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_vpc_basic(vpc):
    """
    Format vpc basic information and returns it as a dictionary
    """

    return {'id': vpc.id, 'name': vpc.name, 'cidr_block': vpc.cidr_block}


def get_vpc_detail(vpc):
    """
    Format vpc detail information and returns it as a dictionary
    """

    return {'id': vpc.id, 'cidr_block': vpc.cidr_block, 'region': vpc.region_id, 'status': vpc.status,
            'vswitch_ids': vpc.vswitch_ids, 'router_id': vpc.router_id, 'name': vpc.name, 'description': vpc.description,
            'creation_time': vpc.creation_time, 'is_default': vpc.is_default, 'user_cidrs': vpc.user_cidrs}


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent', 'list']),
        cidr_block=dict(default='172.16.0.0/16', aliases=['cidr']),
        user_cidr=dict(),
        vpc_name=dict(aliases=['name']),
        description=dict(),
        vpc_id=dict(),
        is_default=dict(type='bool'),
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_vpc.')

    vpc_conn = vpc_connect(module)

    # Get values of variable
    state = module.params['state']
    vpc_id = module.params['vpc_id']
    is_default = module.params['is_default']
    vpc_name = module.params['vpc_name']
    description = module.params['description']
    cidr_block = module.params['cidr_block']
    user_cidr = module.params['user_cidr']

    if str(description).startswith('http://') or str(description).startswith('https://'):
        module.fail_json(msg='description can not start with http:// or https://')
    if str(vpc_name).startswith('http://') or str(vpc_name).startswith('https://'):
        module.fail_json(msg='vpc_name can not start with http:// or https://')

    changed = False
    vpc = None
    vpcs = []
    vpcs_basic = []
    vpcs_by_opts = []

    try:
        page = 1
        pagesize = 50
        while True:
            vpc_list = vpc_conn.get_all_vpcs(vpc_id=vpc_id, is_default=is_default, pagenumber=page, pagesize=pagesize)
            if vpc_list is not None and len(vpc_list) > 0:
                for curVpc in vpc_list:
                    vpcs.append(curVpc)
                    vpcs_basic.append(get_vpc_basic(curVpc))

                    if curVpc.id == vpc_id:
                        vpc = curVpc
                    if vpc_name and cidr_block:
                        if curVpc.name == vpc_name and curVpc.cidr_block == cidr_block:
                            vpcs_by_opts.append(curVpc)
                    elif vpc_name and curVpc.name == vpc_name:
                        vpcs_by_opts.append(curVpc)
                    elif cidr_block and curVpc.cidr_block == cidr_block:
                        vpcs_by_opts.append(curVpc)

            if vpc_list is None or len(vpc_list) < pagesize:
                break
            page += 1

    except VPCResponseError as e:
        module.fail_json(msg='Unable to retrieve vpc, error: {0}'.format(e))

    if not vpc and len(vpcs_by_opts) == 1:
        vpc = vpcs_by_opts[0]

    if len(vpcs_by_opts) > 1:
        vpcs = vpcs_by_opts

    if state == 'present':
        try:
            if not vpc:
                client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
                vpc = vpc_conn.create_vpc(cidr_block=cidr_block, user_cidr=user_cidr, vpc_name=vpc_name,
                                          description=description, client_token=client_token)
            else:
                vpc = vpc.update(name=vpc_name, description=description, user_cidr=user_cidr)
            changed = True
        except VPCResponseError as e:
            module.fail_json(msg='Unable to create or modify vpc, error: {0}'.format(e))

        module.exit_json(changed=changed, vpc_id=vpc.id, vpc=get_vpc_detail(vpc))

    elif state == 'absent':
        if vpc:
            try:
                changed = vpc.delete()
                module.exit_json(changed=changed, vpc_id=vpc.id)
            except VPCResponseError as ex:
                module.fail_json(msg='Unable to delete vpc: {0}, error: {1}'.format(vpc.id, ex))

        module.exit_json(changed=changed, msg="Please specify a vpc by using 'vpc_id', 'vpc_name' or 'cidr_block',"
                                              "and expected vpcs: %s" % vpcs_basic)

    elif state == 'list':
        vpc_ids = []
        vpcs_detail = []
        if vpc:
            module.exit_json(changed=False, vpcs=[get_vpc_detail(vpc)], vpc_ids=[vpc.id], total=1)

        for vpc in vpcs:
            vpc_ids.append(vpc.id)
            vpcs_detail.append(get_vpc_detail(vpc))
        module.exit_json(changed=False, vpcs=vpcs_detail, vpc_ids=vpc_ids, total=len(vpcs))

    else:
        module.fail_json(msg='The expected state: {0}, {1} and {2}, but got {3}.'.format("present", "absent", "list", state))


if __name__ == '__main__':
    main()

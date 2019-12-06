#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: alicloud_vpc
version_added: "1.0.9"
short_description: Create, Query or Delete Vpc. Query Vswitch.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix 'ali' will be more concise
  alternative: Use M(ali_vpc) instead
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
vpc:
    description: info about the VPC that was created or deleted
    returned: always
    type: complex
    contains:
        cidr_block:
            description: The CIDR of the VPC
            returned: always
            type: string
            sample: 10.0.0.0/8
        creation_time:
            description: The time the VPC was created.
            returned: always
            type: string
            sample: 2018-06-24T15:14:45Z
        description:
            description: The VPC description.
            returned: always
            type: string
            sample: "my ansible vpc"
        id:
            description: alias of 'vpc_id'.
            returned: always
            type: string
            sample: vpc-c2e00da5
        is_default:
            description: indicates whether this is the default VPC
            returned: always
            type: bool
            sample: false
        state:
            description: state of the VPC
            returned: always
            type: string
            sample: available
        tags:
            description: tags attached to the VPC, includes name
            returned: always
            type: complex
            sample:
        user_cidrs:
            description: The custom CIDR of the VPC
            returned: always
            type: list
            sample: []
        vpc_id:
            description: VPC resource id
            returned: always
            type: string
            sample: vpc-c2e00da5
        vpc_name:
            description: Name of the VPC
            returned: always
            type: string
            sample: my-vpc
        vrouter_id:
            description: The ID of virtual router which in the VPC
            returned: always
            type: string
            sample: available
        vswitch_ids:
            description: List IDs of virtual switch which in the VPC
            returned: always
            type: list
            sample: [vsw-123cce3, vsw-34cet4v]
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


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        cidr_block=dict(default='172.16.0.0/16', aliases=['cidr']),
        user_cidrs=dict(type='list'),
        vpc_name=dict(aliases=['name']),
        description=dict(),
        vpc_id=dict(),
        is_default=dict(type='bool'),
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_vpc.')

    vpc_conn = vpc_connect(module)

    # Get values of variable
    state = module.params['state']
    vpc_id = module.params['vpc_id']
    vpc_name = module.params['vpc_name']
    description = module.params['description']
    user_cidrs = module.params['user_cidrs']

    if str(description).startswith('http://') or str(description).startswith('https://'):
        module.fail_json(msg='description can not start with http:// or https://')
    if str(vpc_name).startswith('http://') or str(vpc_name).startswith('https://'):
        module.fail_json(msg='vpc_name can not start with http:// or https://')

    changed = False
    vpc = None

    if vpc_id:
        try:
            vpc = vpc_conn.get_vpc_attribute(vpc_id)
        except VPCResponseError as e:
            module.fail_json(msg='Retrieving vpc by id {0} got an error: {1}'.format(vpc_id, e))

    if state == 'absent':
        if not vpc:
            module.exit_json(changed=changed, vpc={})

        try:
            module.exit_json(changed=vpc.delete(), vpc={})
        except VPCResponseError as ex:
            module.fail_json(msg='Unable to delete vpc {0}, error: {1}'.format(vpc.id, ex))

    if not vpc:
        params = module.params
        params['client_token'] = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
        try:
            vpc = vpc_conn.create_vpc(params)
            module.exit_json(changed=True, vpc=vpc.get().read())
        except VPCResponseError as e:
            module.fail_json(msg='Unable to create vpc, error: {0}'.format(e))

    if not vpc_name:
        vpc_name = vpc.vpc_name
    if not description:
        description = vpc.description
    if not user_cidrs:
        user_cidrs = vpc.user_cidrs['user_cidr']

    try:
        if vpc.modify(vpc_name, description, user_cidrs):
            changed = True
        module.exit_json(changed=changed, vpc=vpc.get().read())
    except VPCResponseError as e:
        module.fail_json(msg='Unable to modify vpc {0}, error: {1}'.format(vpc_id, e))


if __name__ == '__main__':
    main()

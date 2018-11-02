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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_vswitch
version_added: "2.8"
short_description: Manage subnet in Alibaba Cloud virtual private cloud(VPC)
description:
    - Manage subnet in Alibaba Cloud virtual private cloud(VPC).
      If an VSwitch ID or cidr block with VPC id is provided, the existing VSwitch (if any) will be modified.
options:
  state:
    description:
      -  Create or delete vswitch.
    choices: ['present', 'absent']
    default: 'present'
  zone_id:
    description:
      - Aliyun availability zone ID which to launch the vswitch or list vswitches.
        It is required when creating a new vswitch.
    aliases: [ 'availability_zone', 'alicloud_zone' ]
  vpc_id:
    description:
      - The ID of a VPC to which that Vswitch belongs. It is required when creating a new vswitch.
  cidr_block:
    description:
      - The CIDR block representing the Vswitch e.g. 10.0.0.0/8. The value must be sub cidr_block of Vpc.
        It is required when creating a new vswitch.
  vswitch_name:
    description:
      - The name of vswitch, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, "_" or "-".
        It cannot begin with http:// or https://.
    aliases: [ 'name', 'subnet_name' ]
  description:
    description:
      - The description of vswitch, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
  vswitch_id:
    description:
      - VSwitch ID. It is used to manage the existing VSwitch. Required when C(present=absent).
    aliases: ['subnet_id', 'id']
requirements:
    - "python >= 2.6"
    - "footmark >= 1.7.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"

"""

EXAMPLES = """

# basic provisioning example to create vswitch
- name: create vswitch
  hosts: localhost
  connection: local
  tasks:
    - name: create vswitch
      ali_vswitch:
        cidr_block: '{{ cidr_blok }}'
        name: 'my-vsw'
        vpc_id: 'vpc-abc12345'
      register: result
    - debug: var=result

# basic provisioning example to delete vswitch
- name: delete vswitch
  hosts: localhost
  connection: local
  tasks:
    - name: delete vswitch
      ali_vswitch:
        vswitch_id: '{{ vswitch_id }}'
        state: 'absent'
      register: result
    - debug: var=result
"""

RETURN = '''
vswitch:
    description: Dictionary of vswitch values
    returned: always
    type: complex
    contains:
        id:
            description: alias of vswitch_id
            returned: always
            type: string
            sample: vsw-b883b2c4
        cidr_block:
            description: The IPv4 CIDR of the VSwitch
            returned: always
            type: string
            sample: "10.0.0.0/16"
        zone_id:
            description: Availability zone of the VSwitch
            returned: always
            type: string
            sample: cn-beijing-a
        state:
            description: state of the Subnet
            returned: always
            type: string
            sample: available
        is_default:
            description: indicates whether this is the default VSwitch
            returned: always
            type: bool
            sample: false
        tags:
            description: tags attached to the Subnet, includes name
            returned: always
            type: dict
            sample: {"Name": "My Subnet", "env": "staging"}
        vpc_id:
            description: the id of the VPC where this VSwitch exists
            returned: always
            type: string
            sample: vpc-67236184
        available_ip_address_count:
            description: number of available IPv4 addresses
            returned: always
            type: string
            sample: 250
        vswitch_id:
            description: VSwitch resource id
            returned: always
            type: string
            sample: vsw-b883b2c4
        subnet_id:
            description: alias of vswitch_id
            returned: always
            type: string
            sample: vsw-b883b2c4
        vswitch_name:
            description: VSwitch resource name
            returned: always
            type: string
            sample: my-vsw
        creation_time:
            description: The time the VSwitch was created.
            returned: always
            type: string
            sample: 2018-06-24T15:14:45Z
'''

import time, inspect
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import VPCResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def uniquely_find_vswitch(connection, module):

    vswitch_id = module.params["vswitch_id"]
    cidr_block = module.params['cidr_block']
    vpc_id = module.params['vpc_id']

    try:
        if not vswitch_id and not cidr_block and not vpc_id:
            return None

        vsws = connection.describe_vswitches(**module.params)
        for v in vsws:
            if vswitch_id and v.vswitch_id == vswitch_id:
                return v
            if cidr_block == v.cidr_block:
                return v
        return None

    except Exception as e:
        module.fail_json(msg=e.message)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        cidr_block=dict(),
        description=dict(),
        zone_id=dict(aliases=['availability_zone','alicloud_zone']),
        vpc_id=dict(),
        vswitch_name=dict(aliases=['name', 'subnet_name']),
        vswitch_id=dict(aliases=['subnet_id', 'id']),
    ))

    module = AnsibleModule(argument_spec=argument_spec,
                           required_if=([
                               ('state', 'absent', ['vswitch_id'])
                           ])
                           )

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_vswitch.')

    vpc = vpc_connect(module)

    # Get values of variable
    state = module.params['state']
    vswitch_name = module.params['vswitch_name']
    description = module.params['description']

    changed = False
    vswitch = uniquely_find_vswitch(vpc, module)

    if state == 'absent':
        if not vswitch:
            module.exit_json(changed=changed, vswitch={})
        try:
            changed = vswitch.delete()
            module.exit_json(changed=changed, vswitch={})
        except VPCResponseError as ex:
            module.fail_json(msg='Unable to delete vswitch: {0}, error: {1}'.format(vswitch.id, ex))

    if str(description).startswith('http://') or str(description).startswith('https://'):
        module.fail_json(msg='description can not start with http:// or https://')

    if str(vswitch_name).startswith('http://') or str(vswitch_name).startswith('https://'):
        module.fail_json(msg='vswitch_name can not start with http:// or https://')

    if not vswitch:
        try:
            params = module.params
            params['client_token'] = "Ansible-Alicloud-{0}-{1}".format(hash(str(module.params)), str(time.time()))
            vswitch = vpc.create_vswitch(**params)
            module.exit_json(changed=True, vswitch=vswitch.get().read())
        except VPCResponseError as e:
            module.fail_json(msg='Unable to create VSwitch, error: {0}'.format(e))

    if not vswitch_name:
        vswitch_name = vswitch.vswitch_name
    if not description:
        description = vswitch.description
    try:
        if vswitch.modify(name=vswitch_name, description=description):
            changed = True
    except VPCResponseError as e:
        module.fail_json(msg='Unable to modify vswitch attribute, error: {0}'.format(e))

    module.exit_json(changed=changed, vswitch=vswitch.get().read())


if __name__ == '__main__':
    main()

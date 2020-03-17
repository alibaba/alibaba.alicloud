#!/usr/bin/python
# -*- coding: utf-8 -*-

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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_ram_role
version_added: "2.9"
short_description: Create, Delete, Update Ram Role in Alibaba Cloud.
description:
    - Create, Delete, Update Role in Alibaba Cloud.
    - An unique ali_ram_role module is determined by parameters role_name. 
options:        
  state:
    description:
      - If I(state=present), role will be created.
      - If I(state=present), and assume_role_policy_document exists, role will be updated.
      - If I(state=absent), role will be removed.
    choices: ['present', 'absent']
    default: 'present'
    type: str
  role_name:
    description:
      - The name of the RAM role. The specified name can be up to 64 characters in length. Format(^[a-zA-Z0-9\. @\-]+$)
      - This is used to determine if the Ram role already exists.
    aliases: ['name']
    required: True
    type: str
  assume_role_policy_document:
    description:
      - The policy text that specifies one or more entities entrusted to assume the RAM role. 
        The trusted entity can be an Alibaba Cloud account, Alibaba Cloud service, or identity provider (IdP).
      - Required when C(state=present)
    type: str
    aliases: ['policy']
  description:
    description:
      - The description of the RAM role. The description can be up to 1,024 characters in length.
    type: str
requirements:
    - "python >= 3.6"
    - "footmark >= 1.17.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Changed. Create a role
  ali_ram_role:
    role_name: ansible
    policy: '{"Statement": [{"Action": "sts:AssumeRole","Effect": "Allow","Principal": {"Service": ["rds.aliyuncs.com"]}}],"Version": "1"}'
    description: create for ansible

- name: Changed. Update role
  ali_ram_role:
    role_name: ansible
    policy: '{"Statement": [{"Action": "sts:AssumeRole","Effect": "Allow","Principal": {"Service": ["ecs.aliyuncs.com"]}}],"Version": "1"}'

- name: Changed. Delete role
  ali_ram_role:
    state: absent
    role_name: ansible
"""

RETURN = '''
user:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        arn:
            description: The Alibaba Cloud Resource Name (ARN) of the RAM role.
            returned: always
            type: string
            sample: acs:ram::123456789012****:role/ECSAdmin
        assume_role_policy_document:
            description: The policy text that specifies one or more entities entrusted to assume the RAM role.
            returned: always
            type: string
            sample: { "Statement": [ { "Action": "sts:AssumeRole", "Effect": "Allow", "Principal": { "RAM": "acs:ram::123456789012****:root" } } ], "Version": "1" }
        create_date:
            description: The date and time when the RAM role was created.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
        description:
            description: The description of the RAM role.
            returned: always
            type: string
            sample: ECS administrator
        role_id:
            description: The ID of the RAM role.
            returned: always
            type: string
            sample: 901234567890****
        role_name:
            description: The name of the RAM role.
            returned: always
            type: string
            sample: ECSAdmin
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RAMResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def role_exists(module, ram_conn, role_name):
    try:
        for r in ram_conn.list_roles():
            if r.read()['name'] == role_name:
                return r
        return None
    except Exception as e:
        module.fail_json(msg="Failed to describe Roles: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        role_name=dict(type='str', required=True, aliases=['name']),
        assume_role_policy_document=dict(type='str', aliases=['policy']),
        description=dict(type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    ram_conn = ram_connect(module)

    # Get values of variable
    state = module.params['state']
    role_name = module.params['role_name']
    assume_role_policy_document = module.params['assume_role_policy_document']
    changed = False

    # Check if role exists
    role = role_exists(module, ram_conn, role_name)

    if state == 'absent':
        if not role:
            module.exit_json(changed=changed, role={})
        try:
            module.exit_json(changed=role.delete(), role={})
        except RAMResponseError as ex:
            module.fail_json(msg='Unable to delete role {0}, error: {1}'.format(role_name, ex))

    if not role:
        try:
            role = ram_conn.create_role(**module.params)
            module.exit_json(changed=True, role=role.read())
        except RAMResponseError as e:
            module.fail_json(msg='Unable to create role, error: {0}'.format(e))

    if assume_role_policy_document:
        try:
            changed = role.update_policy(policy=assume_role_policy_document)
            module.exit_json(changed=changed, role=role.get().read())
        except RAMResponseError as e:
            module.fail_json(msg='Unable to update role policy, error: {0}'.format(e))


if __name__ == '__main__':
    main()

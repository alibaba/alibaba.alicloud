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
module: ali_ram_access_key
version_added: "2.9"
short_description: Create, Delete, Update Ram Access Key in Alibaba Cloud.
description:
    - Create, Delete Ram Access Key and Update status in Alibaba Cloud.
    - This module does not support idempotence
options:
  state:
    description:
      - If I(state=present), access key will be created.
      - If I(state=present) and user_access_key_id exists, access key will be updated.
      - If I(state=absent), access key will be removed.
    choices: ['present', 'absent']
    default: 'present'
    type: str
  user_name:
    description:
      - The username of the RAM user.
    required: True
    type: str
    aliases: ['name']
  user_access_key_id:
    description:
      - The ID of the AccessKey to be updated. Required when update access key.
    type: str
  status:
    description:
      - The status of the AccessKey. Required when update access key.
    choices: ['Active', 'Inactive']
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
- name: Changed. Create access key
  ali_ram_access_key:
    user_name: ansible
  register: access

- name: Changed. Update access key
  ali_ram_access_key:
    user_access_key_id: '{{ user_access_key_id }}'
    user_name: ansible
    status: Inactive

- name: Changed. Delete access key
  ali_ram_access_key:
    state: absent
    user_access_key_id: '{{ user_access_key_id }}'
    user_name: ansible
"""

RETURN = '''
user:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        access_key_id:
            description: The AccessKeyId.
            returned: always
            type: string
            sample: 0wNEpMMlzy7s****
        access_key_secret:
            description: The AccessKeySecret.
            returned: When create access key
            type: string
            sample: PupkTg8jdmau1cXxYacgE736PJ****
        create_date:
            description: The date and time when the AccessKey was created.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
        status:
            description: The status of the AccessKey.
            returned: always
            type: string
            sample: Active
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RAMResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def list_access_key(module, ram_conn, user_name):
    try:
        res = []
        exists = ram_conn.list_access_keys(user_name=user_name)
        if exists:
            for ak in exists:
                res.append(ak.read())
        return res
    except Exception as e:
        module.fail_json(msg="Failed to get profile: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        user_name=dict(type='str', required=True, aliases=['name']),
        user_access_key_id=dict(type='str'),
        status=dict(type='str', choices=['Active', 'Inactive'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    ram_conn = ram_connect(module)

    # Get values of variable
    state = module.params['state']
    user_access_key_id = module.params['user_access_key_id']
    user_name = module.params['user_name']
    aks = list_access_key(module, ram_conn, user_name)

    changed = False

    if state == 'absent':
        try:
            module.exit_json(changed=ram_conn.delete_access_key(**module.params), access_key={})
        except RAMResponseError as e:
            module.fail_json(msg='Unable to delete access_key, error: {}'.format(e))

    if user_access_key_id:
        try:
            res = ram_conn.update_access_key(**module.params)
            if res:
                module.exit_json(changed=True, access_key=res.read())
            module.exit_json(changed=changed, access_key={})
        except Exception as e:
            module.fail_json(msg='Unable to update access_key, error: {}'.format(e))
    if len(aks) < 2:
        try:
            access_key = ram_conn.create_access_key(**module.params)
            module.exit_json(changed=True, access_key=access_key.read())
        except RAMResponseError as e:
            module.fail_json(msg='Unable to create access_key, error: {0}'.format(e))

    module.exit_json(changed=changed, access_key=aks)


if __name__ == '__main__':
    main()

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
module: ali_ram_user
version_added: "2.9"
short_description: Create, Delete, Update Ram User in Alibaba Cloud.
description:
    - Create, Delete, Update Ram User in Alibaba Cloud.
    - An unique ali_ram_user module is determined by parameters user_name. 
options:
  state:
    description:
      - If I(state=present), user will be created.
      - If I(state=absent), user will be removed.
    choices: ['present', 'absent']
    default: 'present'
    type: str
  user_name:
    description:
      - The username. It must be 1 to 64 characters in length.
      - This is used to determine if the user already exists.
    aliases: ['name']
    required: True
    type: str
  display_name:
    description:
      - The display name. It must be 1 to 128 characters in length.
    type: str
  mobile_phone:
    description:
      - The mobile phone number of the RAM user. International area code-mobile phone number.
    type: str
    aliases: ['phone']
  email:
    description:
      - The email address of the RAM user.
    type: str
  comments:
    description:
      - The comment. It must be 1 to 128 characters in length.
    type: str
  new_user_name:
    description:
      - The new username of the new RAM user. It must be 1 to 64 characters in length.
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
- name: Changed. Create a new user
  ali_ram_user:
    user_name: ansible
    display_name: ab
    mobile_phone: 18988888888
    email: 11288222@qq.com
    comments: ansible_test

- name: Changed. Update user
  ali_ram_user:
    user_name: '{{ user_name }}'
    new_user_name: ansible2

- name: Changed. Delete user
  ali_ram_user:
    state: absent
    user_name: '{{ user_name}}'

"""

RETURN = '''
user:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        user_name:
            description: The username.
            returned: always
            type: string
            sample: Alice
        name:
            description: alias of 'user_name'.
            returned: always
            type: string
            sample: Alice
        user_id:
            description: The ID of the RAM user.
            returned: always
            type: string
            sample: 122748924538****
        id:
            description: alias of 'user_id'.
            returned: always
            type: string
            sample: 122748924538****
        mobile_phone:
            description: The mobile phone number of the RAM user.
            returned: always
            type: string
            sample: 86-1860000****
        phone:
            description: alias of 'mobile_phone'.
            returned: always
            type: string
            sample: vpc-c2e00da5
        email:
            description: The email address of the RAM user.
            returned: always
            type: string
            sample: alice@example.com
        display_name:
            description: The display name.
            returned: always
            type: string
            sample: Alice
        create_date:
            description: The date and time when the RAM user was created.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
        comments:
            description: The comment.
            returned: always
            type: string
            sample: ansible test
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


def user_exists(module, ram_conn, user_name):
    try:
        for u in ram_conn.list_users():
            if u.name == user_name:
                return u
        return None
    except Exception as e:
        module.fail_json(msg="Failed to describe Users: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        user_name=dict(type='str', required=True, aliases=['name']),
        display_name=dict(type='str'),
        mobile_phone=dict(type='str', aliases=['phone']),
        email=dict(type='str'),
        comments=dict(type='str'),
        new_user_name=dict(type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    ram_conn = ram_connect(module)

    # Get values of variable
    state = module.params['state']
    user_name = module.params['user_name']
    changed = False

    # Check if user exists
    user = user_exists(module, ram_conn, user_name)

    if state == 'absent':
        if not user:
            module.exit_json(changed=changed, user={})
        try:
            module.exit_json(changed=user.delete(), user={})
        except RAMResponseError as ex:
            module.fail_json(msg='Unable to delete user {0}, error: {1}'.format(user_name, ex))

    if not user:
        try:
            user = ram_conn.create_user(**module.params)
            module.exit_json(changed=True, user=user.read())
        except RAMResponseError as e:
            module.fail_json(msg='Unable to create user, error: {0}'.format(e))

    try:
        res = user.update(**module.params)
        if res:
            module.exit_json(changed=True, user=res.read())
    except RAMResponseError as e:
        module.fail_json(msg='Unable to update user, error: {0}'.format(e))

    module.exit_json(changed=changed, user=user.read())


if __name__ == '__main__':
    main()

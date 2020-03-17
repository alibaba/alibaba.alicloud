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
module: ali_ram_login_profile
version_added: "2.9"
short_description: Create, Delete, Update Ram login profile in Alibaba Cloud.
description:
    - Create, Delete, Update Ram login profile in Alibaba Cloud.
options:
  state:
    description:
      - If I(state=present), ram login profile will be created.
      - If I(state=present) and login profile exists, it will be updated.
      - If I(state=absent), ram login profile will be removed.
    default: 'present'
    choices: ['present', 'absent']
    type: str
  user_name:
    description:
      - The username.
    aliases: ['name']
    required: True
    type: str
  password:
    description:
      - The password.
    type: str 
  new_password:
    description:
      - The new password. Required when update password.
    type: str
  password_reset_required:
    description:
      - Specifies whether you need to change your password upon logon.
    default: False
    type: bool
  mfa_bind_required:
    description:
      - Specifies whether you need to attach an MFA device upon the next logon.
    default: False
    type: bool
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
- name: Changed. Create login profile
  ali_ram_login_profile:
    user_name: ansible
    password: YourPassword
    password_reset_required: True

- name: Changed. update login profile
  ali_ram_login_profile:
    user_name: ansible
    password: YourNewPassword

- name: Changed. Delete login profile
  ali_ram_login_profile:
    state: absent
    user_name: ansible
"""

RETURN = '''
user:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        create_date:
            description: The creation time.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
        mfabind_required:
            description: Indicates that you must attach an MFA device.
            returned: always
            type: bool
            sample: False
        password_reset_required:
            description: Indicates that you must change your password upon next logon.
            returned: always
            type: bool
            sample: False
        user_name:
            description: The username.
            returned: always
            type: string
            sample: Alice
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RAMResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def profile_exists(module, ram_conn, user_name):
    try:
        return ram_conn.get_login_profile(user_name=user_name)
    except Exception as e:
        module.fail_json(msg="Failed to get profile: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        user_name=dict(type='str', required=True, aliases=['name']),
        password=dict(type='str'),
        new_password=dict(type='str'),
        password_reset_required=dict(type='bool', default=False),
        mfa_bind_required=dict(type='bool', default=False)
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    ram_conn = ram_connect(module)

    # Get values of variable
    state = module.params['state']
    user_name = module.params['user_name']
    changed = False

    # Check if profile exists
    profile = profile_exists(module, ram_conn, user_name)
    # module.exit_json(changed=True, profile=profile.read())

    if state == 'absent':
        if not profile:
            module.exit_json(changed=changed, profile={})
        try:
            changed = ram_conn.delete_login_profile(**module.params)
            module.exit_json(changed=changed, profile={})
        except RAMResponseError as ex:
            module.fail_json(msg='Unable to delete profile error: {}'.format(ex))

    if not profile:
        try:
            profile = ram_conn.create_login_profile(**module.params)
            module.exit_json(changed=True, profile=profile.read())
        except RAMResponseError as e:
            module.fail_json(msg='Unable to create profile, error: {0}'.format(e))

    try:
        changed = profile.update(**module.params)
        module.exit_json(changed=changed, profile=profile.read())
    except Exception as e:
        module.fail_json(msg='Unable to update profile, error: {0}'.format(e))


if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_ram_login_profile_info
version_added: "2.9"
short_description: Gather info on ram login profile in Alibaba Cloud.
description:
     - Gather info on ram login profile in Alibaba Cloud.
options:
  user_name:
    description:
      - The username.
    type: str
    required: True
    aliases: ['name']
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.17.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Get the existing login profile.
  ali_ram_login_profile_info:
    user_name: ansible

'''

RETURN = '''
users:
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


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        user_name=dict(type='str', required=True, aliases=['name'])
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    user_name = module.params['user_name']
    try:
        profile = ram_connect(module).get_login_profile(user_name=user_name)
        module.exit_json(changed=False, profile=profile.read())
    except Exception as e:
        module.fail_json(msg=str("Unable to get profile, error:{0}".format(e)))


if __name__ == '__main__':
    main()

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
module: ali_ram_user_info
version_added: "2.9"
short_description: Gather info on ram users in Alibaba Cloud.
description:
     - Gather info on ram users in Alibaba Cloud. support name_prefix to filter users.
options:
  name_prefix:
    description:
      - Use a User name prefix to filter Users.
    type: str
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

- name: Get infos about all Users
  ali_ram_user_info:

- name: Get infos about a particular User using name_prefix
  ali_ram_user_info:
    name_prefix: "ansible"

'''

RETURN = '''
users:
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
        update_date:
            description: The date and time when the user information was modified.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
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
        name_prefix=dict(type='str'))
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    name_prefix = module.params['name_prefix']

    try:
        users = []
        for user in ram_connect(module).list_users():
            if name_prefix and not user.name.startswith(name_prefix):
                continue
            users.append(user.read())
        module.exit_json(changed=False, users=users)
    except Exception as e:
        module.fail_json(msg=str("Unable to list users, error:{0}".format(e)))


if __name__ == '__main__':
    main()

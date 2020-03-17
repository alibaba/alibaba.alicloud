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
module: ali_ram_role_info
version_added: "2.9"
short_description: Gather info on ram role in Alibaba Cloud.
description:
     - Gather info on ram role in Alibaba Cloud. support name_prefix to filter roles.
options:
  name_prefix:
    description:
      - Use a Role name prefix to filter Roles.
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

- name: Get the existing role
  ali_ram_role_info:
    name_prefix: ansible

'''

RETURN = '''
roles:
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
            sample: {"Statement": [{ "Action": "sts:AssumeRole", "Effect": "Allow", "Principal": { "RAM": "acs:ram::123456789012****:root" }}], "Version": "1"}
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
        roles = []
        for role in ram_connect(module).list_roles():
            if name_prefix and not role.name.startswith(name_prefix):
                continue
            roles.append(role.get().read())
        module.exit_json(changed=False, roles=roles)
    except Exception as e:
        module.fail_json(msg=str("Unable to list roles, error:{0}".format(e)))


if __name__ == '__main__':
    main()

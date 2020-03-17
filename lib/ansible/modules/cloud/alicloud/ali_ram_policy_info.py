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
module: ali_ram_policy_info
version_added: "2.9"
short_description: Gather info on ram policy in Alibaba Cloud.
description:
     - Gather info on ram policy in Alibaba Cloud. support name_prefix to filter policies.
options:
  name_prefix:
    description:
      - Use a policy name prefix to filter policies.
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
- name: Get the existing policy
  ali_ram_policy_info:
    name_prefix: ansible_oss

- name: Get the all policy
  ali_ram_policy_info:
'''

RETURN = '''
policies:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        attachment_count:
            description: The number of times that the policy is referenced.
            returned: always
            type: int
            sample: 0
        create_date:
            description: The date and time when the policy was created.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
        default_version:
            description: The default version.
            returned: always
            type: string
            sample: v1
        description:
            description: The policy description.
            returned: always
            type: string
            sample: OSS administrator
        policy_name:
            description: The policy name.
            returned: always
            type: string
            sample: OSS-Administrator
        name:
            description: alias of 'policy_name'.
            returned: always
            type: string
            sample: OSS-Administrator
        policy_type:
            description: The policy type.
            returned: always
            type: string
            sample: Custom
        update_date:
            description: The date and time when the policy was modified.
            returned: always
            type: string
            sample: 2015-01-23T12:33:18Z
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
        policies = []
        for policy in ram_connect(module).list_policies():
            if name_prefix and not policy.name.startswith(name_prefix):
                continue
            policies.append(policy.read())
        module.exit_json(changed=False, policies=policies)
    except Exception as e:
        module.fail_json(msg=str("Unable to list groups, error:{0}".format(e)))


if __name__ == '__main__':
    main()

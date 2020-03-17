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
module: ali_dns_group_info
version_added: "2.9"
short_description: Gather facts on domain group of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the group itself.
options:
  group_id:
    description:
      - Id of group, specify it to filter group.
    type: str
    aliases: ['id']
  name_prefix:
    description:
      - Use a Group name prefix to filter groups.
    type: str
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Get the existing group with name_prefix
  ali_dns_group_info:
    name_prefix: '{{ name }}'
  register: groups

- name: Get the existing group with group_id
  ali_dns_group_info:
    group_id: '{{ group_id }}'
  register: groups

- name: Get the existing group with domain_count
  ali_dns_group_info:
    domain_count: '{{ domain_count }}'
  register: groups

- name: Retrieving all dns group
  ali_dns_group_info:
'''

RETURN = '''
ids:
    description: List all group's id after operating group.
    returned: when success
    type: list
    sample: [ "group-2zegusms7jwd94lq7ix8o", "group-2ze5hrb3y5ksx5oa3a0xa" ]
groups:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        count:
            description: alias of 'domain_count'.
            returned: always
            type: int
            sample: 0
        domain_count:
            description: Number of domain names in the group .
            returned: always
            type: dict
            returned: always
            type: int
            sample: 0
        group_id:
            description: The id of group.
            returned: always
            type: string
            sample: xxxxxxxxxx
        id:
            description: alias of 'group_id'.
            returned: always
            type: string
            sample: xxxxxxxxxx
        group_name:
            description: Name of group.
            returned: always
            type: string
            sample: ansible_test
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, dns_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import DNSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        name_prefix=dict(type='str'),
        group_id=dict(type='str', aliases=['id']),
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    name_prefix = module.params['name_prefix']
    group_id = module.params['group_id']

    try:
        groups = []
        ids = []
        for _dns in dns_connect(module).describe_domain_groups():
            if name_prefix and not _dns.name.startswith(name_prefix):
                continue
            if group_id and _dns.id != group_id:
                continue
            groups.append(_dns.read())
            ids.append(_dns.id)

        module.exit_json(changed=False, groups=groups, ids=ids)
    except Exception as e:
        module.fail_json(msg=str("Unable to get dns group, error:{0}".format(e)))


if __name__ == '__main__':
    main()

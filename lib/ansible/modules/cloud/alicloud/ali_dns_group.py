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
module: ali_dns_group
version_added: "2.9"
short_description: Configure Alibaba Cloud DNS (DNS)
description:
    - Create, Delete Alicloud cloud DNS group(DNS group).
      It supports updating group name.
options:
  lang:
    description:
      - The language which you choose
    type: str
  group_name:
    description:
      - Give the name of group when create DNS group and Use this parameter to guarantee idempotence.
    aliases: ['name']
    type: str
  state:
    description:
      -  Whether or not to create, delete DNS group.
    choices: ['present', 'absent']
    default: 'present'
    type: str
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Changed. Create dns group.
  ali_dns_group:
    group_name: '{{ group_name }}'

- name: Changed. Deleting dns group
  ali_dns_group:
    group_name: '{{ group_name }}'
    state: absent
"""

RETURN = '''
groups:
    description: info about the DNS group that was created or deleted
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


def dns_group_exists(module, dns_conn, group_name):
    try:
        for v in dns_conn.describe_domain_groups():
            if v.name == group_name:
                return v
        return None
    except Exception as e:
        module.fail_json(msg="Failed to describe DNS group: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_name=dict(type='str', aliases=['name']),
        lang=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent']),
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_dns_group.')

    dns_conn = dns_connect(module)

    # Get values of variable
    state = module.params['state']
    group_name = module.params['group_name']
    changed = False

    dns_group = dns_group_exists(module, dns_conn,group_name)

    if state == 'absent':
        if not dns_group:
            module.exit_json(changed=changed, groups={})
        try:
            module.exit_json(changed=dns_group.delete(), groups={})
        except DNSResponseError as ex:
            module.fail_json(msg='Unable to delete dns group{0}, error: {1}'.format(dns_group.id, ex))

    if not dns_group:
        params = module.params
        try:
            dns_group = dns_conn.add_domain_group(**params)
            if dns_group:
                changed = True
            module.exit_json(changed=changed, groups=dns_group.get().read())
        except DNSResponseError as e:
            module.fail_json(msg='Unable to create dns group, error: {0}'.format(e))

    module.exit_json(changed=changed, groups=dns_group.read())


if __name__ == '__main__':
    main()

#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_security_group_facts
version_added: "1.5.0"
short_description: Gather facts on security group of Alibaba Cloud ECS.
description:
  - This module fetches data from the Open API in Alicloud.
    The module must be called from within the ECS security group itself.

options:
  group_ids:
    description:
      - A list of ECS security group IDs.
    aliases: ["ids"]
  group_name:
    description:
      - Name of the security group.
    aliases: ["name"]
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value.
        The filter keys can be all of request parameters. See U(https://www.alibabacloud.com/help/doc-detail/35748.htm) for parameter details.
        Filter keys can be same as request parameter name or be lower case and use underscores (_) or dashes (-) to
        connect different words in one parameter. "Tag.n.Key" and "Tag.n.Value" use new filter 'tags' instead and
        it should be a dict.
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.

# Gather facts about all security groups
- ali_security_group_facts:

# Gather facts about all security groups in a specific VPC
- ali_security_group_facts:
    filters:
      vpc-id: vpc-12345678

# Gather facts about a security group
- ali_security_group_facts:
    group_name: example-1

# Gather facts about a security group by id
- ali_security_group_facts:
    group_ids: sg-12345678

# Gather facts about a security group with multiple filters, also mixing the use of underscores as filter keys
- ali_security_group_facts:
    group_name: example-2
    filters:
      vpc_id: vpc-12345678

# Gather facts about any security group with a tag key Name and value Example.
- ali_security_group_facts:
    filters:
      tags:
        name: Example
'''

RETURN = '''
ids:
    description: list IDs of security groups
    returned: always
    type: list
    sample: ["sg-2ze12578be1ls4wcjhfd", "sg-2ze28n1vj1iqztxp7p6h"]
groups:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        description:
            description: The Security Group description.
            returned: always
            type: string
            sample: "my ansible group"
        group_name:
            description: Security group name
            sample: "my-ansible-group"
            type: string
            returned: always
        group_id:
            description: Security group id
            sample: sg-abcd1234
            type: string
            returned: always
        id:
            description: Alias of "group_id".
            sample: sg-abcd1234
            type: string
            returned: always
        inner_access_policy:
            description: Whether can access each other in one security group.
            sample: True
            type: bool
            returned: always
        tags:
            description: Tags associated with the security group
            sample:
            Name: My Security Group
            From: Ansible
            type: dict
            returned: always
        vpc_id:
            description: ID of VPC to which the security group belongs
            sample: vpc-abcd1234
            type: string
            returned: always
        permissions:
            description: Inbound rules associated with the security group.
            sample:
                - create_time: "2018-06-28T08:45:58Z"
                  description: "None"
                  dest_cidr_ip: "None"
                  dest_group_id: "None"
                  dest_group_name: "None"
                  dest_group_owner_account: "None"
                  direction: "ingress"
                  ip_protocol: "TCP"
                  nic_type: "intranet"
                  policy: "Accept"
                  port_range: "22/22"
                  priority: 1
                  source_cidr_ip: "0.0.0.0/0"
                  source_group_id: "None"
                  source_group_name: "None"
                  source_group_owner_account: "None"
            type: list
            returned: always
        permissions_egress:
            description: Outbound rules associated with the security group.
            sample:
                - ip_protocol: -1
                  ip_ranges:
                    - create_time: "2018-06-28T08:45:59Z"
                      description: "NOne"
                      dest_cidr_ip: "192.168.0.54/32"
                      dest_group_id: "None"
                      dest_group_name: "None"
                      dest_group_owner_account: "None"
                      direction: "egress"
                      ip_protocol: "TCP"
                      nic_type: "intranet"
                      policy: "Accept"
                      port_range: "80/80"
                      priority: 1
                      source_cidr_ip: "None"
                      source_group_id: "None"
                      source_group_name: "None"
                      source_group_owner_account: "None"
            type: list
            returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect


try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_name=dict(type='str', aliases=['name']),
        group_ids=dict(type='list', aliases=['ids']),
        filters=dict(type='dict')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    ecs = ecs_connect(module)

    group_ids = module.params['group_ids']
    name = module.params['group_name']

    changed = False
    result = []
    try:
        security_groups = ecs.get_all_security_groups(module.params)
        group_ids = []
        for sg in security_groups:
            if group_ids and sg.security_group_id not in group_ids:
                continue
            if name and sg.security_group_name != name:
                continue
            result.append(sg.read())
            group_ids.append(sg.id)
    except ECSResponseError as e:
        module.fail_json(msg='Error in get_all_security_groups: {0}'.format(e))

    module.exit_json(changed=changed, ids=group_ids, groups=result)


if __name__ == '__main__':
    main()

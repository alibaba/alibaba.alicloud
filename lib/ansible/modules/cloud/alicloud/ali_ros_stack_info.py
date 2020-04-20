#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017-present Alibaba Group Holding Limited. He Steven
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

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_ros_stack_info
short_description: "Get ROS Stack detailed information."
description:
    -  Get cloud resource stack detailed information of Alibaba Cloud ROS.
author:
    - "Steven"
options:
  stack_ids:
    description:
      - A list of ROS IDs that exist in your account.
    aliases: ["ids"]
    type: list
    elements: str
  name_prefix:
    description:
      - Use a ROS name prefix to filter ROSs.
    type: str
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value. The filter keys can be
        all of request parameters. See U(https://www.alibabacloud.com/help/doc-detail/132117.htm) for parameter details.
    type: dict
requirements:
    - "python >= 3.6"
    - "footmark >= 1.20.0"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
-   name: Get ROS Stack Info By ids
    ali_ros_stack_info:
        stack_ids:
          - f83226ec-b0f2-4c78-8139-99fe24f36f2b
          - 0d87e1b4-c54f-4f3e-abed-2678e661c0a5
    
-   name: Get ROS Stack Info By name_prefix
    ali_ros_stack_info:
        name_prefix: kong_stack
"""
RETURN = """
ids:
    description: Return ROS stack ids.
    returned: always
    type: list
    sample: [ "f83226ec-b0f2-4c78-8139-99fe24f36f2b", "0d87e1b4-c54f-4f3e-abed-2678e661c0a5" ]
stacks:
    description: Return ROS stack detailed information.
    returned: always
    type: complex
    contains:
        create_time: 
            description: ROS stack create time.
            returned: always
            type: str
            sample: '2020-04-09T01:21:26'
        disable_rollback:
            description: ROS stack Rollback options config.
            returned: always
            type: bool
            sample: false
        region_id:
            description: ROS stack resources region location. 
            returned: always
            type: str
            sample: cn-beijing
        stack_id: 
            description: ROS stack resources id.
            returned: always
            type: str
            sample: f15d848b-236c-4791-8487-75a24ab93a6b
        stack_name: 
            description: ROS stack resources name.
            returned: always
            type: str
            sample: stack_2020-04-09
        status: 
            description: ROS stack resources status.
            returned: always
            type: str
            sample: CREATE_COMPLETE
        status_reason: 
            description: ROS stack resources status description.
            returned: always
            type: str
            sample: Stack CREATE completed successfully
        timeout_in_minutes: 60
            description: ROS stack resources create timeout time.
            returned: always
            type: int
            sample: 60
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ros_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ROSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(
        dict(
            stack_ids=dict(type='list', elements='str', aliases=['ros_stack_ids']),
            name_prefix=dict(type='str'),
            filters=dict(type='dict')
        )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_ros.')
    stack_ids = module.params['stack_ids']
    if not stack_ids:
        stack_ids = []
    filters = module.params['filters']
    if not filters:
        filters = {}
    name_prefix = module.params.get('name_prefix')
    ros_infos = []
    ros_ids = []
    try:
        ros_conn = ros_connect(module)
        if stack_ids:
            for stack_id in stack_ids:
                filters['stack_id'] = stack_id
                stack_info = ros_conn.list_stacks(**filters)[0]
                if stack_info.get('stack_id') not in ros_ids:
                    ros_infos.append(stack_info)
                    ros_ids.append(stack_info.get('stack_id'))
        elif name_prefix:
            all_stack_infos = ros_conn.list_stacks(**filters)
            for stack_info in all_stack_infos:
                if stack_info.get('stack_name').startswith(name_prefix) and stack_info.get(
                        'stack_id') not in ros_ids:
                    ros_infos.append(stack_info)
                    ros_ids.append(stack_info.get('stack_id'))
        module.exit_json(ids=ros_ids, stacks=ros_infos, changed=False)
    except Exception as e:
        module.fail_json(msg="Get ros stack info failed, and got an error: {0}.".format(e))


if __name__ == "__main__":
    main()


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

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module:ali_ros
short_description:"Manage cloud resource stack of Alibaba Cloud ROS"
author:
    - "Steven"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.9.0"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
-   hosts: localhost
    remote_user: root
    tasks:
        -   name: Get ROS Stack Info
            ali_ros_info:
                alicloud_access_key: <your-alicloud-access-key-id>
                alicloud_secret_key: <your-alicloud-access-secret-key>
                alicloud_region: cn-beijing
                stack_name: create_vpc_2020-04-08_test
"""
RETURN = """
ros:
    CreateTime: 2020-04-09T01:21:26
    DisableRollback: false
    RegionId: cn-beijing
    StackId: f15d848b-236c-4791-8487-75a24ab93a6b
    StackName: stack_2020-04-09_bcx
    Status: CREATE_COMPLETE
    StatusReason: Stack CREATE completed successfully
    TimeoutInMinutes: 60
"""
import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ros import ros_argument_spec, connect_to_ros

HAS_FOOTMARK = False

try:
    from footmark.exception import ROSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ros_argument_spec()
    argument_spec.update(
        dict(
            stack_name=dict(required=True, type='str'),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_ros.')
    stack_name = module.params.get('stack_name')

    if not re.search('^[a-zA-Z][a-zA-Z0-9_\-]{0,255}$', stack_name):
        module.fail_json(
            msg='Stack name "%s" is invalid and exceeds 255 character limit. Stack names must contain only '
                'alphanumeric characters and hyphens and must start with an alphabetic character.' % stack_name)
    try:
        ros_stack = connect_to_ros(module)
        ros_stack_info = ros_stack.query_stack_id_by_name(stack_name=stack_name, get_info=True)
        module.exit_json(ros=ros_stack_info, changed=False)
    except Exception as e:
        module.fail_json(msg="Get ros stack info failed, and got an error: {0}.".format(e))


if __name__ == "__main__":
    main()

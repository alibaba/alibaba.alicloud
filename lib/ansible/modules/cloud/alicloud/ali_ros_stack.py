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
module: ali_ros_stack
short_description: "Management cloud resource stack of Alibaba Cloud ROS"
description:
    - Create, Delete and Modify for ROS Stack.
author:
    - "Steven"
options:
  state:
    description:
      -  Whether or not to create, delete, modify ROS.
    choices: ['present', 'absent']
    type: str
    default: 'present'
    required: True
  stack_name:
    description:
      -  ROS stack resources name.
    type: str
    required: True
  template:
    description:
      -  Ros stack resources template file path.
    type: str
  timeout_in_minutes:
    description:
      -  Ros stack resources create timeout time.
    type: int
    default: 60
  template_parameters:
    description:
      -  Ros stack resources template parameters.
    type: dict
requirements:
    - "python >= 3.6"
    - "footmark >= 1.20.0"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
  - name: Changed. Create Ros Stack
    ali_ros_stack:
      stack_name: vpc_2020-04-08_test
      template: /tmp/create_vpn.json
      timeout_in_minutes: 60
      template_parameters:
        CidrBlock: 192.168.0.0/16
        VpcName: DemoVpc

  - name: Changed. Update Ros Stack
      ali_ros_stack:
        stack_name: vpc_2020-04-08_test
        template: /tmp/update_vpc.json
        timeout_in_minutes: 60
        template_parameters:
          CidrBlock: 192.168.0.0/16
          VpcName: UpdateVpc

  - name: Changed. Delete Ros Stack
      ali_ros_stack:      
        state: absent        
        stack_name: vpc_2020-04-08_test
"""
RETURN = """
stack:
    description: Return Ros stack detailed information.
    returned: always
    type: complex
    contains:
        create_time: 
            description: Ros stack create time.
            returned: always
            type: str
            sample: '2020-04-09T01:21:26'
        disable_rollback:
            description: Ros stack Rollback options config.
            returned: always
            type: bool
            sample: false
        region_id:
            description: Ros stack resources region location. 
            returned: always
            type: str
            sample: cn-beijing
        stack_id: 
            description: Ros stack resources id.
            returned: always
            type: str
            sample: f15d848b-236c-4791-8487-75a24ab93a6b
        stack_name: 
            description: Ros stack resources name.
            returned: always
            type: str
            sample: stack_2020-04-09
        status: 
            description: Ros stack resources status.
            returned: always
            type: str
            sample: CREATE_COMPLETE
        status_reason: 
            description: Ros stack resources status description.
            returned: always
            type: str
            sample: Stack CREATE completed successfully
        timeout_in_minutes: 60
            description: Ros stack resources create timeout time.
            returned: always
            type: int
            sample: 60
"""

import re
import json
import ruamel.yaml
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ros_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ROSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_template_body(template_path):
    if template_path.endswith('.yml') or template_path.endswith('.yaml'):
        yaml_body = open(template_path, 'r').read()
        yd = ruamel.yaml.load(yaml_body, ruamel.yaml.RoundTripLoader)
        template_body = json.dumps(yd, indent=2)
    else:
        template_body = open(template_path, 'r').read()
    return template_body


def get_template_params(input_params):
    template_parameters_dict = [{"ParameterKey": k, "ParameterValue": v} for k, v in input_params.items()]
    return template_parameters_dict


def ros_exists(ros_conn, stack_name):
    ros_stack = ros_conn.list_stacks(stack_names=[stack_name], get_one=True)
    if not ros_stack:
        return None
    else:
        return ros_stack.get('stack_id')


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(
        dict(
            stack_name=dict(required=True, type='str'),
            template_parameters=dict(type='dict'),
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            template=dict(type='str'),
            timeout_in_minutes=dict(default=60, type='int')
        )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_ros.')

    try:
        stack_name = module.params.get('stack_name')
        parameterss = get_template_params(module.params.get('template_parameters')) if \
            module.params.get('template_parameters') else []
        state = module.params.get('state')
        template_body = get_template_body(module.params.get('template')) if module.params.get('template') else None
        template_type = module.params.get('template').split('.')[1] if module.params.get(
            'template') and '.' in module.params.get('template') else ""
        timeout_in_minutes = module.params.get('timeout_in_minutes')
        if not re.search('^[a-zA-Z][a-zA-Z0-9_\-]{0,255}$', stack_name):
            module.fail_json(
                msg='Stack name "%s" is invalid and exceeds 255 character limit. Stack names must contain only '
                    'alphanumeric characters and hyphens and must start with an alphabetic character.' % stack_name)
        if template_type:
            if not template_type == "json":
                module.fail_json(
                    msg='Input template type : %s error, Please check it' % template_type)
        ros_conn = ros_connect(module)
        changed = False
        # Check if ROS stack exists
        stack_id = ros_exists(ros_conn, stack_name)
        params = {'stack_name': stack_name,
                  'parameterss': parameterss,
                  'template_body': template_body,
                  'timeout_in_minutes': timeout_in_minutes}

        if state == 'absent':
            if not stack_id:
                module.exit_json(changed=changed, ros={})
            try:
                del_res = ros_conn.delete_stack(stack_id=stack_id)
                module.exit_json(stack={}, changed=del_res)
            except ROSResponseError as e:
                module.fail_json(msg='Unable to delete ros, error: {0}'.format(e))
        elif state == 'present' and not stack_id:
            try:
                create_res = ros_conn.create_stack(**params)
                module.exit_json(changed=True, stack=create_res)
            except ROSResponseError as e:
                module.fail_json(msg='Unable to create ros, error: {0}'.format(e))
        else:
            try:
                params['stack_id'] = stack_id
                del params['stack_name']
                update_res = ros_conn.update_stack(**params)
                module.exit_json(changed=True, stack=update_res)
            except ROSResponseError as e:
                module.fail_json(msg='Unable to update ros, error: {0}'.format(e))
    except Exception as e:
        module.fail_json(msg="Manage ros stack failed, and got an error: {0}.".format(e))


if __name__ == '__main__':
    main()


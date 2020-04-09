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
        -   name: Management ROS Stack
            ali_ros:
                alicloud_access_key: <your-alicloud-access-key-id>
                alicloud_secret_key: <your-alicloud-access-secret-key>
                alicloud_region: cn-beijing
                state: "{{ stack_state | default('create') }}"
                stack_name: create_vpc_2020-04-08_test
                template: /tmp/ros_template.json
                create_timeout: 60
                template_parameters:
                  CidrBlock: 192.168.0.0/16
                  VpcName: DemoVpc
"""
RETURN = """
ros:
    StackId: 423AC3F6-A078-4FA0-8371-A48DE83F2C7C
    RequestId: 8dd5b6ec-74b9-4291-b065-35ba92b0409a
"""

import re
import json
import ruamel.yaml
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ros import ros_argument_spec, connect_to_ros

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


def main():
    argument_spec = ros_argument_spec()
    argument_spec.update(
        dict(
            stack_name=dict(required=True, type='str'),
            template_parameters=dict(required=False, type='dict', default={}),
            state=dict(default='create', choices=['create', 'delete', 'update']),
            template=dict(default=None, required=False),
            template_url=dict(default=None, required=False),
            create_timeout=dict(default=60, required=False)
        )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_ros.')

    try:
        stack_name = module.params.get('stack_name')
        template_parameters = module.params.get('template_parameters')
        state = module.params.get('state')
        template = module.params.get('template')
        template_type = template.split('.')[1] if template and '.' in template else ""
        template_url = module.params.get('template_url')
        create_timeout = module.params.get('create_timeout')
        if not re.search('^[a-zA-Z][a-zA-Z0-9_\-]{0,255}$', stack_name):
            module.fail_json(
                msg='Stack name "%s" is invalid and exceeds 255 character limit. Stack names must contain only '
                    'alphanumeric characters and hyphens and must start with an alphabetic character.' % stack_name)
        if template_type:
            if not (template_type == "json" or template_type == "yml" or template_type == "yaml"):
                module.fail_json(
                    msg='Input template type : %s error, Please check it' % template_type)
        ros_stack = connect_to_ros(module)
        stack_id = ros_stack.query_stack_id_by_name(stack_name=stack_name)
        if state == 'create' or state == 'update':
            if template is None and template_url is None:
                if state == 'create' or state == 'update':
                    module.fail_json(
                        msg='Module parameter "template" or "template_url" is required if "state" is "create" or "update".')
            if template is not None:
                template_path = template
                template_body = get_template_body(template_path)
            else:
                template_body = None
            if template_parameters is not None:
                parameters = get_template_params(template_parameters)
            else:
                parameters = []
            if state == 'create':
                if stack_id:
                    module.fail_json(msg='Create Stack %s already exists' % stack_name)
                else:
                    res = ros_stack.create_stack(stack_name, template_body, parameters, create_timeout, template_type)
            elif state == 'update':
                if not stack_id:
                    module.fail_json(msg='Update Stack %s is not exists' % stack_name)
                else:
                    res = ros_stack.update_stack(stack_id, template_body, parameters, create_timeout, template_type)
        elif state == 'delete':
            if not stack_id:
                module.fail_json(msg='Delete Stack %s does not exists' % stack_name)
            else:
                res = ros_stack.delete_stack(stack_id)
        else:
            res = "Please check your input state type."
        module.exit_json(ros=res, changed=False)
    except Exception as e:
        module.fail_json(msg="Manage ros stack  failed, and got an error: {0}.".format(e))


if __name__ == '__main__':
    main()

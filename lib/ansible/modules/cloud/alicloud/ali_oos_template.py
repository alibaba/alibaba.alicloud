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

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_oos_template
short_description: Configure Alibaba Cloud Operation Orchestration Service(OOS)
description:
    - Create, Delete, Update template.
    - It supports updating template content.
    - An unique ali_oos_template module is determined by parameters template_name.
options:
  state:
    description:
      - If I(state=present), template will be created.
      - If I(state=absent), template will be removed.
      - If I(state=present), template and content exists, it will be updated.
    choices: ['present', 'absent']
    type: str
    default: 'present'
  content:
    description:
      - Template content. JSON or YAMl format, limited to 64 kb.
      - Required when C(state=present).
    type: str
  template_name:
    description:
      - Template name. The content is limited to letters, numbers, dashes and underscores, 
        with a length of 200 characters, and cannot start with ALIYUN, ACS, ALIBABA, ALICLOUD.
    type: str
    aliases: ['name']
  template_id:
    description:
      - Template id. Required when C(template_name="") and (C(state=absent) or update resource).
    type: str
    aliases: ['id'] 
  tags:
    description:
      - A hash/dictionaries of template tags. C({"key":"value"})
    type: dict
  purge_tags:
    description:
      - Delete existing tags on the template that are not specified in the task.
        If True, it means you have to specify all the desired tags on each task affecting a template.
    default: False
    type: bool
requirements:
    - "python >= 3.6"
    - "footmark >= 1.20.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
  - "Li Xue (@lixue323)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.

- name: Changed. Create a new template with json
  ali_oos_template:
    content: '{"FormatVersion": "OOS-2019-06-01", "Description": "Describe instances of given status", "Parameters": {"Status": {"Type": "String", "Description": "(Required) The status of the Ecs instance."}}, "Tasks": [{"Properties": {"Parameters": {"Status": "\{\{ Status \}\}"}, "API": "DescribeInstances", "Service": "Ecs"}, "Name": "foo", "Action": "ACS::ExecuteApi"}]}'
    template_name: 'template_name'
    tags:
      From: 'ansible'

- name: Changed. Create a new template with yml
  ali_oos_template:
    content:
      FormatVersion: OOS-2019-06-01
      Description: Describe instances of given status
      Parameters:
        Status:
          Type: String
          Description: (Required) The status of the Ecs instance.
      Tasks:
        - Properties:
            Parameters:
              Status: '\{\{ Status \}\}'
            API: DescribeInstances
            Service: Ecs
          Name: foo
          Action: 'ACS::ExecuteApi'
    template_name: '{{ name }}'
    tags:
      From: 'ansible'

- name: Changed. Update template
  ali_oos_template:
    content: '{"FormatVersion": "OOS-2019-06-01", "Description": "Describe instances", "Parameters": {"Status": {"Type": "String", "Description": "(Required) The status of the Ecs instance."}}, "Tasks": [{"Properties": {"Parameters": {"Status": "\{\{ Status \}\}"}, "API": "DescribeInstances", "Service": "Ecs"}, "Name": "foo", "Action": "ACS::ExecuteApi"}]}'
    template_name: 'template_name'

- name: Changed. Delete template
  ali_oos_template:
    state: absent
    template_name: 'template_name'
"""

RETURN = '''
template:
    description: info about the template  that was created, deleted, updated
    returned: always
    type: complex
    contains:
        content:
            description: The content of template.
            returned: always
            type: str
            sample: ""
        created_by:
            description: The Creator of template.
            returned: always
            type: str
            sample: root(1300000)
        created_date:
            description: The Template creation date.
            returned: always
            type: str
            sample: "2019-05-16T10:26:14Z"
        description:
            description: The template description.
            returned: always
            type: str
            sample: Describe instances of given status
        has_trigger:
            description: Triggered successfully or not.
            returned: always
            type: bool
            sample: true
        hash:
            description: the SHA256 of template content.
            returned: always
            type: str
            sample: 4bc7d7a21b3e003434b9c223f6e6d2578b5ebfeb5be28c1fcf8a8a1b11907bb4
        share_type:
            description: The type of template.
            returned: always
            type: str
            sample: Private
        tags:
            description: tags attached to the template.
            returned: always
            type: dict
            sample: {"k1":"v1","k2":"v2"}
        template_format:
            description: The format of the template, Json or Yaml.
            returned: always
            type: str
            sample: JSON
        template_id:
            description: The id of template.
            returned: always
            type: str
            sample: t-94753d38
        id:
            description: aliases of template_id.
            returned: always
            type: str
            sample: t-94753d38
        template_name:
            description: The name of the template.
            returned: always
            type: str
            sample: MyTemplate
        name:
            description: aliases of template_name.
            returned: always
            type: str
            sample: MyTemplate
        template_version:
            description: The version of template.
            returned: always
            type: str
            sample: v1
        version:
            description: aliases of template_version.
            returned: always
            type: str
            sample: v1
        updated_by:
            description: Template updated by.
            returned: always
            type: str
            sample: root(130000)
        updated_date:
            description: The Date of template updated.
            returned: always
            type: str
            sample: "2019-05-16T10:26:14Z"
'''

import time
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, oos_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import OOSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def template_exists(module, oos_conn):
    try:
        res = oos_conn.list_templates()
        temp = None
        if res:
            for t in res:
                if module.params.get('template_name') and t.template_name == module.params['template_name']:
                    temp = t.get()
                if module.params.get('template_id') and t.template_id == module.params['template_id']:
                    temp = t.get()
        return temp

    except Exception as e:
        module.fail_json(msg="Failed to list templates: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        content=dict(type='str'),
        template_name=dict(type='str', aliases=['name']),
        template_id=dict(type='str', aliases=['id']),
        tags=dict(type='dict'),
        purge_tags=dict(type='bool', default=False)
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    oos_conn = oos_connect(module)

    # Get values of variable
    state = module.params['state']

    changed = False

    # Check if template exists
    temp = template_exists(module, oos_conn)
    content = module.params['content']
    if content:
        content = json.dumps(eval(content.replace('\\', '')))
        module.params['content'] = content
    if state == 'absent':
        if not temp:
            module.exit_json(changed=changed, tempalte={})
        try:
            module.exit_json(changed=temp.delete(), tempalte={})
        except OOSResponseError as e:
            module.fail_json(msg='Unable to delete template {0}, error: {1}'.format(module.params['template_name'], e))

    if not temp:
        params = module.params
        params['client_token'] = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
        try:
            temp = oos_conn.create_template(**params)
            module.exit_json(changed=True, template=temp.read())
        except OOSResponseError as e:
            module.fail_json(msg='Unable to create template, error: {0}'.format(e))

    if content:
        try:
            if temp.update(content=content):
                changed = True
        except Exception as e:
            module.fail_json(msg="{0}".format(e))

    tags = module.params['tags']
    if module.params['purge_tags']:
        if not tags:
            tags = temp.tags
        try:
            if temp.remove_tags(tags):
                changed = True
            module.exit_json(changed=changed, template=temp.read())
        except Exception as e:
            module.fail_json(msg="{0}".format(e))

    if tags:
        try:
            if temp.add_tags(tags):
                changed = True
        except Exception as e:
            module.fail_json(msg="{0}".format(e))
    module.exit_json(changed=changed, template=temp.read())


if __name__ == '__main__':
    main()

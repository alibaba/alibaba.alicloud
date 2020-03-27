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

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_oos_template_info
short_description: Gather info on template of Alibaba Cloud OOS.
description:
     - This module fetches data from the Open API in Alicloud.
options:
  tags:
    description:
      - A hash/dictionaries of template tags. C({"key":"value"})
    type: dict
  name_prefix:
    description:
      - Use a template name prefix to filter templates.
    type: str
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value. The filter keys can be
        all of request parameters. See U(https://www.alibabacloud.com/help/zh/doc-detail/120763.htm) for parameter details.
        Filter keys can be same as request parameter name or be lower case and use underscore ("_") or dash ("-") to
        connect different words in one parameter. 'ExecutionId' will be appended to I(execution_id) automatically.
    type: dict
requirements:
    - "python >= 3.6"
    - "footmark >= 1.20.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
  - "Li Xue (@lixue323)"
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.

- name: No Changed. Get template with name_prefix
  ali_oos_template_info:
    name_prefix: 'ansible-testacc'

- name: No Changed. Get template with tags
  ali_oos_template_info:
    tags:
      from: 'ansible'

- name: No Changed. Get template with filters
  ali_oos_template_info:
    filters:
      share_type: Private
'''

RETURN = '''
names:
    description: The names of templates.
    returned: always
    type: list
    sample:
        - MyTemplate
          MyTemplate1
templates:
    description: info about the template  that was created, deleted, updated
    returned: always
    type: complex
    contains:
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
        risky_tasks:
            description: The risky task of template.
            returned: always
            type: complex
            contains:
                api:
                    description: The name of risky api.
                    returned: always
                    type: str
                    sample: DeleteInstance
                service:
                    description: The product that risky api belongs to.
                    returned: always
                    type: str
                    sample: ECS             
                task:
                    description: The task that risky api belongs to.
                    returned: always
                    type: list
                    sample: ["parenttask1"]
                template:
                    description: The template that risky task belongs to.
                    returned: always
                    type: list
                    sample: ["deleteInstanceTask1"]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, oos_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import OOSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        filters=dict(type='dict'),
        name_prefix=dict(type='str', aliases=['name']),
        tags=dict(type='dict')
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    templates = []
    names = []
    tags = module.params['tags']
    name_prefix = module.params['name_prefix']
    filters = module.params['filters']
    if not filters:
        filters = {}
    try:
        for template in oos_connect(module).list_templates(**filters):
            if name_prefix and not str(template.name).startswith(name_prefix):
                continue
            if tags:
                flag = False
                for key, value in list(tags.items()):
                    if key in list(template.tags.keys()) and value == template.tags[key]:
                        flag = True
                if not flag:
                    continue
            templates.append(template.get().read())
            names.append(template.get().name)
        module.exit_json(changed=False, names=names, templates=templates)
        # module.exit_json(changed=False, names=names, templates=templates)
    except Exception as e:
        module.fail_json(msg=str("Unable to get templates, error:{0}".format(e)))


if __name__ == '__main__':
    main()

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
module: ali_oos_execution_info
short_description: Gather info on execution of Alibaba Cloud OOS.
description:
     - This module fetches data from the Open API in Alicloud.
options:
  name_prefix:
    description:
      - Use a template name prefix to filter executions.
    type: str
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value. The filter keys can be
        all of request parameters. See U(https://www.alibabacloud.com/help/zh/doc-detail/120772.htm) for parameter details.
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

- name: No Changed. Get executions with template name prefix
  ali_oos_execution_info:
    name_prefix: 'ACS-ECS'

- name: No Changed. Get executions with filters
  ali_oos_execution_info:
    filters:
      status: Success
'''

RETURN = '''
ids:
    description: ids of the executions that was started, notified
    returned: always
    type: list
    sample: ['exec-xxxyyy']
executions:
    description: info about the executions that was started, notified
    returned: always
    type: complex
    contains:
        execution_id:
            description: The id of execution.
            returned: always
            type: str
            sample: exec-xxxyyy
        id:
            description: aliases of execution_id.
            returned: always
            type: str
            sample: exec-xxxyyy
        is_parent:
            description: Have child task or not.
            returned: always
            type: bool
            sample: false
        loop_mode:
            description: The loop mode.
            returned: always
            type: str
            sample: Automatic
        mode:
            description: mode of execution.
            returned: always
            type: str
            sample: Automatic
        out_puts:
            description: The output of execution.
            returned: always
            type: str
            sample: {"InstanceId":"i-xxx"}
        parameters:
            description: The parameters of execution.
            returned: always
            type: str
            sample: {"Status":"Running"}
        parent_execution_id:
            description: The id of parent execution.
            returned: always
            type: str
            sample: exec-xxxx
        ram_role:
            description: The ram role of execution.
            returned: always
            type: str
            sample: OOSServiceRole
        safety_check:
            description: The security check mode.
            returned: always
            type: str
            sample: Skip
        description:
            description: The description of execution.
            returned: always
            type: str
            sample: run instance
        start_date:
            description: The start date of the execution.
            returned: always
            type: str
            sample: "2019-05-16T10:26:14Z"
        status:
            description: The status of the execution.
            returned: always
            type: str
            sample: Success
        status_message:
            description: The message of the status.
            returned: always
            type: str
            sample: ""
        template_id:
            description: The id of the template.
            returned: always
            type: str
            sample: t-1bd341007f
        template_name:
            description: The name of the template.
            returned: always
            type: str
            sample: MyTemplate
        template_version:
            description: The version of template.
            returned: always
            type: str
            sample: v1
        update_date:
            description: The update date of template.
            returned: always
            type: str
            sample: "2019-05-16T10:26:14Z"
        executed_by:
            description: The template executor.
            returned: always
            type: str
            sample: root(13092080xx12344)
        end_date:
            description: The end date of execution.
            returned: always
            type: str
            sample: "2019-05-16T10:26:14Z"
        task_name:
            description: The name of task.
            returned: always
            type: str
            sample: waitForReady
        task_execution_id:
            description: The id of task execution.
            returned: always
            type: str
            sample: exec-xxxyyy.0001
        task_action:
            description: The action of task.
            returned: always
            type: str
            sample: ACS::WaitFor
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
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    executions = []
    ids = []
    name_prefix = module.params['name_prefix']
    filters = module.params['filters']
    if not filters:
        filters = {}
    try:
        for e in oos_connect(module).list_executions(**filters):
            if name_prefix and not str(e.name).startswith(name_prefix):
                continue
            executions.append(e.read())
            ids.append(e.id)
        module.exit_json(changed=False, ids=ids, executions=executions)
    except Exception as e:
        module.fail_json(msg=str("Unable to get executions, error:{0}".format(e)))


if __name__ == '__main__':
    main()

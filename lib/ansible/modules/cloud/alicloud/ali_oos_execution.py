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
module: ali_oos_execution
short_description: Configure Execution Alibaba Cloud Operation Orchestration Service(OOS)
description:
    - Create, Delete, Notify, Cancel Execution.
options:
  state:
    description:
      - If I(state=present), execution will be started.
      - If I(state=absent), execution will be deleted.
      - If I(state=cancel), execution will be canceled.
      - If I(state=notify), It will notify a pending execution of how to run next.
    choices: ['present', 'absent', 'cancel', 'notify']
    type: str
    default: 'present'
  task_execution_id:
    description:
      - The id of task execution.
    type: str
  task_name:
    description:
      - The name of task execution.
    type: str
  notify_note:
    description:
      - The note of notify.
    type: str
  loop_item:
    description:
      - Loop child nodes corresponding to Item data.
    type: str
  execution_status:
    description:
      - The status of execution.
      - Required when C(notify_type=CompleteExecution)
    type: str
  notify_type:
    description:
      - The type of notify. 
      - If C(notify_type=Approve), approval of pending execution. If you know the execution risks of high-risk operations, and allow them to perform.
      - If C(notify_type=Reject), reject execution pending approval. If high-risk operations are not allowed to perform tasks.
      - If C(notify_type=ExecuteTask), specifies the start of the execution of a task, suitable for Debug mode. May need to cooperate with I(parameters).
      - If C(notify_type=CancelTask), cancel current task execution, applicable to when C(mode=Debug).
      - If C(notify_type=CompleteExecution), manually terminate execution in a debug mode. Can be used with the I(execution_status) to specify the status of execution termination.
    choices: ['Approve', 'Reject', 'ExecuteTask', 'CancelTask', 'CompleteExecution']
    type: str
  executed_by:
    description:
      - The user executed execution.
      - when you want to cancel,delete or notify executions, you can pass it to filter executions, except it, 
        filter params supported include (I(template_name), I(status), I(execution_ids))
    type: str
  status:
    description:
      - The status of execution.
      - when you want to cancel,delete or notify executions, you can pass it to filter executions, except it, 
        filter params supported include (I(template_name), I(executed_by), I(execution_ids))
    type: str
  safety_check:
    description:
      - Security check mode.
      - If C(safety_check=Skip), means that the customer understands the risk and can perform any action without confirmation, 
        regardless of the level of risk. Effective when C(mode=Automatic).
      - If C(safety_check=ConfirmEveryHighRiskAction), will ask the customer to confirm each high-risk action. 
        The client confirms or cancels by calling the NotifyExecution interface.
    type: str
    default: ConfirmEveryHighRiskAction
    choices: ['Skip', 'ConfirmEveryHighRiskAction']
  parent_execution_id:
    description:
      - The id of parent execution.
    type: str
  parameters:
    description:
      - Consists of a collection of parameters.
    type: dict
  mode:
    description:
      - The execution mode.
    type: str
    choices: ['Debug', 'Automatic']
  loop_mode:
    description:
      - The Loop mode.
    type: str
  template_name:
    description:
      - The name of template.
      - when you want to start a execution, It is required.
      - when you want to cancel,delete or notify executions, you can pass it to filter executions, except it, 
        filter params supported include (I(status), I(executed_by), I(execution_ids))
    type: str
  description:
    description:
      - The description of execution.
    type: str
  execution_ids:
    description:
      - The ids of executions.
      - when you want to cancel,delete or notify executions, you can pass it to filter executions, except it, 
        filter params supported include (I(status), I(executed_by), I(template_name))
    type: list
    elements: str
  tags:
    description:
      - A hash/dictionaries of template tags. C({"key":"value"})
    type: dict
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

- name: Changed. Start a timed execution that starts and closes instances
  ali_oos_execution:
    template_name: 'ACS-ECS-ScheduleToStartAndStopInstances'
    safety_check: Skip
    description: test execution from ansible
    parameters:
      dailyStartTime: 08:00:00Z
      dailyStopTime: dailyStopTime
      weekdays: '2'
      targets:
        Type: ResourceIds
        ResourceIds: 
          - 'instances_id'
    tags:
      From: ansible

- name: Changed. cancel a timed execution
  ali_oos_execution:
    state: cancel
    template_name: 'ACS-ECS-ScheduleToStartAndStopInstances'

- name: Changed. Delete a execution
  ali_oos_execution:
    state: absent
    template_name: 'ACS-ECS-ScheduleToStartAndStopInstances'

- name: Changed. Start a risky execution that deletes instances
  ali_oos_execution:
    template_name: 'ACS-ECS-BulkyDeleteInstances'
    description: test execution from ansible
    parameters:
      force: true
      targets:
        Type: ResourceIds
        ResourceIds:
          - 'instances_id'

- name: Changed. notify a execution
  ali_oos_execution:
    state: notify
    notify_type: Approve
    template_name: 'ACS-ECS-BulkyDeleteInstances'

- name: Changed. Delete a execution
  ali_oos_execution:
    state: absent
    template_name: 'ACS-ECS-BulkyDeleteInstances'
"""

RETURN = '''
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

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, oos_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import OOSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def executions_exists(module, oos_conn):
    try:
        executions = []
        if module.params.get('execution_ids'):
            for i in module.params.get('execution_ids'):
                executions.extend(oos_conn.list_executions(execution_id=i))
        elif module.params.get('params'):
            executions.extend(oos_conn.list_executions(**module.params['params']))
        ids = []
        if executions:
            for e in executions:
                ids.append(e.id)
        else:
            module.fail_json(msg="Failed to list executions, please make sure your params are correct")
        return ids
    except Exception as e:
        module.fail_json(msg="Failed to list templates: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent', 'cancel', 'notify']),
        execution_ids=dict(type='list', elements='str'),
        description=dict(type='str'),
        template_name=dict(type='str', aliases=['name']),
        loop_mode=dict(type='str'),
        mode=dict(type='str', choices=['Debug', 'Automatic']),
        parameters=dict(type='dict'),
        parent_execution_id=dict(type='str'),
        safety_check=dict(type='str', default='ConfirmEveryHighRiskAction', choices=['Skip', 'ConfirmEveryHighRiskAction']),
        tags=dict(type='dict'),

        status=dict(type='str'),
        executed_by=dict(type='str'),

        notify_type=dict(type='str', choices=['Approve', 'Reject', 'ExecuteTask', 'CancelTask', 'CompleteExecution']),
        execution_status=dict(type='str'),
        loop_item=dict(type='str'),
        notify_note=dict(type='str'),
        task_execution_id=dict(type='str'),
        task_name=dict(type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    oos_conn = oos_connect(module)

    # Get values of variable
    state = module.params['state']

    template_name = module.params['template_name']
    status = module.params['status']
    executed_by = module.params['executed_by']
    params = {}

    if template_name:
        params['template_name'] = template_name
    if status:
        params['status'] = status
    if executed_by:
        params['executed_by'] = executed_by
    changed = False
    if params:
        module.params['params'] = params

    if state == 'absent':
        ids = executions_exists(module, oos_conn)
        try:
            if oos_conn.delete_executions(execution_ids=ids):
                changed = True
            module.exit_json(changed=changed, executions={})
        except OOSResponseError as e:
            module.fail_json(msg='Unable to delete executions {0}, error: {1}'.format(str(ids), e))

    elif state == 'cancel':
        ids = executions_exists(module, oos_conn)
        try:
            if ids:
                for i in ids:
                    if oos_conn.cancel_execution(execution_id=i):
                        changed = True
            module.exit_json(changed=changed, executions={})
        except OOSResponseError as e:
            module.fail_json(msg='Unable to cancel executions {0}, error: {1}'.format(str(ids), e))

    elif state == 'present':
        client_token = "Ansible-Alicloud-{0}-{1}".format(hash(str(module.params)), str(time.time()))
        module.params['client_token'] = client_token
        execution = oos_conn.start_execution(**module.params)
        if execution:
            changed = True
        module.exit_json(changed=changed, executions=execution.read())

    else:
        excutions = []
        ids = executions_exists(module, oos_conn)
        if ids:
            for i in ids:
                module.params['execution_id'] = i
                if oos_conn.notify_execution(**module.params):
                    changed = True
                excutions.append(oos_conn.list_executions(execution_id=i)[0].read())

        module.exit_json(changed=changed, excutions=excutions)


if __name__ == '__main__':
    main()

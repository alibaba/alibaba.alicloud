#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com>
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
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_ess_task
version_added: "1.0.9"
short_description: Create or Terminate an scheduled task in ESS.
description:
    - A scheduled task used to execute scaling activity in a scaling group automatically.
    - At most 20 scheduled tasks can be specified in a account.
    - When the trigger of a scheduled task fails because a scaling activity in a scaling group is in progress or
      the scaling group is disabled, the scheduled task is automatically retried within the LaunchExpirationTime;
      otherwise, the scheduled trigger task is abandoned.
    - If multiple tasks are scheduled at similar times to execute the rule of the same group,
      the earliest task triggers the scaling activity first, and other tasks make attempts to execute the rule
      within their Launch Expiration Time because a scaling group executes only one scaling activity at a time.
      If another scheduled task is still making triggering attempts within its Launch Expiration Time after the
      scaling activity is finished, the scaling rule is executed and the corresponding scaling activity is triggered.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix "ali" will be more concise.
  alternative: Use M(ali_ess_task) instead.
options:
    state:
      description:
        - present to create a scheduled task and absent to delete it.
      default: 'present'
      choices: [ 'present', 'absent' ]
    rule_id:
      description:
        - ID of the scaling rule of a scheduled task. Required when C(state=present)
    launch_time:
      description:
        - Time point at which the scheduled task is triggered.
        - The date format follows the ISO8601 standard and uses UTC time. It is in the format of YYYY-MM-DDThh:mmZ.
        - If I(recurrence_type), the time point specified by this attribute is the default time point at which the circle is executed.
          Otherwise, the task is executed once on the designated date and time.
        - A time point 90 days after creation or modification cannot be inputted.
        - Required when C(state=present).
    launch_expiration:
      description:
        - Time period within which the failed scheduled task is retried, in second. Value range [0, 21600].
      default: 600
      aliases: ['expiration']
    name:
      description:
        - Display name of the scheduled task.
        - It must be 2-40 characters (English or Chinese) long, and begin with a number, an upper/lower-case letter
          or a Chinese character and may contain numbers, "_", "-" or ".".
        - Default to scheduled task ID.
      aliases: ['task_name' ]
    description:
      description:
        - Description of the scheduled task, which is 2-200 characters (English or Chinese) long.
    recurrence_type:
      description:
        - Type of the scheduled task to be repeated. Optional values 'Daily', 'Weekly' and 'Monthly'
          to indicates recurrence interval by day, week or month for a scheduled task.
        - I(recurrence_type, recurrence_value, recurrence_endtime) must be specified or not at the same time.
      aliases: [ 'type' ]
      choices: ['Daily', 'Weekly', 'Monthly']
    recurrence_value:
      description:
        - Value of the scheduled task to be repeated.
        - Daily should only supported one value in the range [1,31].
        - Weekly support multiple values. The values of Sunday to Saturday are 0 to 6 in sequence.
          Multiple values shall be separated by a comma ",".
        - Monthly use format A-B and the value range of A and B is 1 to 31, and the B value must be greater than the A value.
        - I(recurrence_type, recurrence_value, recurrence_endtime) must be specified or not at the same time.
      aliases: [ 'value' ]
    recurrence_endtime:
      description:
        - End time of the scheduled task to be repeated.
          The date format follows the ISO8601 standard and uses UTC time. It is in the format of YYYY-MM-DDThh:mmZ.
          A time point 90 days after creation or modification cannot be inputted.
        - I(recurrence_type, recurrence_value, recurrence_endtime) must be specified or not at the same time.
      aliases: [ 'endtime' ]
    enabled:
      description:
        - Whether to enable the scheduled task.
      default: True
      type: bool
    id:
      description:
        - The ID of existing scheduled task.
      aliases: [ 'task_id' ]

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.3.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    rule_id: asr-2zefe4bi0jpctd6z726p
    launch_time: 2018-01-09T15:00Z
    launch_expiration: 300
    recurrence_type: 'Daily'
    recurrence_value: 10
    recurrence_endtime: 2018-02-10T15:00Z
    name: task-from-ansible

  tasks:
    - name: launch scheduled task
      alicloud_ess_task:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        name: '{{ name }}'
        rule_id: '{{ rule.id }}'
        launch_time: '{{ launch_time }}'
        launch_expiration: '{{ launch_expiration }}'
        recurrence_type: '{{ recurrence_type }}'
        recurrence_value: '{{ recurrence_value }}'
        recurrence_endtime: '{{ recurrence_endtime }}'

    - name: delete specified scheduled task
      alicloud_ess_task:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        name: '{{ name }}'
        state: absent

'''

RETURN = '''
id:
    description: Scheduled Task ID.
    returned: expect absent
    type: str
    sample: "cItPa1ec7ii6dryMmEbBnJZP"
name:
    description: Scheduled Task name.
    returned: expect absent
    type: str
    sample: ess-task-foo
task:
    description: The details of a scheduled task.
    returned: expect absent
    type: dict
    sample: {
        "description": null,
        "enabled": true,
        "id": "cItPa1ec7ii6dryMmEbBnJZP", 
        "launch_expiration": 300,
        "launch_time": "2018-01-09T15:00Z",
        "name": "ess-task-foo",
        "recurrence_endtime": "2018-02-10T15:00Z", 
        "recurrence_type": "Daily",
        "recurrence_value": "10",
        "rule_ari": "ari:acs:ess:cn-beijing:1204663572767468:scalingrule/asr-2zefe4bi0jpctd6z726p"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ess_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_details(task):
    return dict(id=task.id,
                name=task.name,
                rule_ari=task.rule_ari,
                description=getattr(task, 'description', None),
                launch_time=task.launch_time,
                launch_expiration=task.launch_expiration,
                recurrence_type=task.recurrence_type,
                recurrence_value=task.recurrence_value,
                recurrence_endtime=task.recurrence_end_time,
                enabled=task.enabled,
                )


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        rule_id=dict(type='str'),
        launch_time=dict(type='str'),
        launch_expiration=dict(type='int', defalut=600, aliases=['expiration']),
        name=dict(type='str', aliases=['task_name']),
        description=dict(type='str'),
        recurrence_type=dict(type='str', choices=['Daily', 'Weekly', 'Monthly'], aliases=['type']),
        recurrence_value=dict(type='str', aliases=['value']),
        recurrence_endtime=dict(type='str', aliases=['endtime']),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        enabled=dict(type='bool', default=True),
        id=dict(type='str', aliases=['task_id'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_ess_task.")

    ess = ess_connect(module)
    state = module.params['state']
    task_id = module.params['id']
    task_name = module.params['name']
    rule_id = module.params['rule_id']
    launch_time = module.params['launch_time']
    launch_expiration = module.params['launch_expiration']
    recurrence_type = module.params['recurrence_type']
    recurrence_value = module.params['recurrence_value']
    recurrence_endtime = module.params['recurrence_endtime']
    enabled = module.params['enabled']
    description = module.params['description']

    # Get scaling rule ari according rule ID
    rule_ari = None
    if rule_id:
        rules = ess.describe_rules(scaling_rule_ids=[rule_id])
        rule_ari = rules[0].ari

    count = 0
    if recurrence_type:
        count += 1
    if recurrence_value:
        count += 1
    if recurrence_endtime:
        count += 1
    if count in (1, 2):
        module.fail_json(msg="'recurrence_type', 'recurrence_value' and 'recurrence_endtime' must be specified or not at the same time")

    changed = False

    current = None
    all_tasks = []
    if task_id or task_name:
        tasks = ess.describe_scheduled_tasks(scheduled_task_ids=[task_id], scheduled_task_names=[task_name],
                                             scaling_rule_aris=[rule_ari])

        if tasks:
            if len(tasks) > 1:
                for task in tasks:
                    all_tasks.append(task.id)
                module.fail_json(msg="There are several scheduled tasks in our record based on name {0}: {1}. "
                                     "Please specified one using 'id' and try again.".format(task_name, all_tasks))
            current = tasks[0]

    if state == 'present':
        if current is None:
            try:
                if not rule_id:
                    module.exit_json(msg="'rule_id': required field when state is present, aborting.")
                if not rule_ari:
                    module.exit_json(msg="There is no scheduled task in our record based on rule id {0}, aborting."
                                         "Please check it and try again.".format(rule_id))
                if not launch_time:
                    module.exit_json(msg="'launch_time': required field when state is present, aborting.")

                current = ess.create_scheduled_task(scaling_rule_ari=rule_ari, launch_time=launch_time, name=task_name,
                                                    description=description, launch_expiration_time=launch_expiration,
                                                    recurrence_type=recurrence_type, recurrence_value=recurrence_value,
                                                    recurrence_end_time=recurrence_endtime, task_enabled=enabled)
                changed = True
            except Exception as e:
                module.fail_json(msg="Create scheduled task got an error: {0}".format(e))

        else:
            try:
                changed = current.modify(scaling_rule_ari=rule_ari, launch_time=launch_time, name=task_name,
                                         description=description, launch_expiration_time=launch_expiration,
                                         recurrence_type=recurrence_type, recurrence_value=recurrence_value,
                                         recurrence_end_time=recurrence_endtime, task_enabled=enabled)
                if changed:
                    current = current.update(validate=True)
            except Exception as e:
                module.fail_json(msg="Modify scheduled rule got an error: {0}".format(e))

        module.exit_json(changed=changed, id=current.id, name=current.name, task=get_details(current))

    if current is None:
        if task_id or task_name:
                module.fail_json(msg="There are no scheduled task in our record based on id {0} or name {1}. "
                                     "Please check it and try again.".format(task_id, task_name))
        module.fail_json(msg='Please specify a scheduled task that you want to terminate by field id or name, aborting')

    try:
        module.exit_json(changed=current.terminate())
    except Exception as e:
        module.fail_json(msg='Delete scheduled task {0} got an error: {1}'.format(current.id, e))


if __name__ == '__main__':
    main()

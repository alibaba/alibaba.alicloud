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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_ess_rule
version_added: "1.5.0"
short_description: Create or Terminate an scaling rule in ESS.
description:
    - A scaling rule defines specific scaling actions, for example, adding or removing n ECS instances.
      If the execution of a scaling rule results in a number of ECS instances in the scaling group that is less than
      the MinSize or greater than the MaxSize, Auto Scaling automatically adjusts the number of ECS instances to be
      added or removed by executing the "Adjust scaling group instance quantity to MinSize"
      or "Adjust scaling group instance quantity to MaxSize" rule.
options:
    state:
      description:
        - present to create a scaling rule and absent to delete it.
      default: 'present'
      choices: [ 'present', 'absent' ]
    name:
      description:
        - The name of scaling rule.
        - It must contain 2-40 English or Chinese characters, and start with a number, a letter in upper or
          lower case or a Chinese character, and it can contain numbers, "_", "-" or ".".
        - Default to scaling rule Id.
      aliases: ['rule_name']
    adjustment_type:
      description:
        - Adjustment mode of a scaling rule.
        - QuantityChangeInCapacity used to increase or decrease a specified number of ECS instances;
        - PercentChangeInCapacity used to increase or decrease a specified proportion of ECS instances;
        - TotalCapacity used to adjust the quantity of ECS instances in the current scaling group to a specified value.
        - Required when C(state=present).
      aliases: [ 'type' ]
      choices: ['QuantityChangeInCapacity', 'PercentChangeInCapacity', 'TotalCapacity']
    adjustment_value:
      description:
        - Adjusted value of a scaling rule.
        - QuantityChangeInCapacity to (0, 100] U (-100, 0];
        - PercentChangeInCapacity to [0, 10000] U [-10000, 0];
        - TotalCapacity to [0, 100].
        - Required when C(state=present).
      aliases: [ 'value' ]
    cooldown:
      description:
        - Cool-down time of a scaling rule. Value range to [0, 86400], in seconds. The default value is empty.
    group_id:
      description:
        - ID of the scaling group of a scaling rule. Required when C(state=present).
      aliases: [ 'scaling_group_id' ]
    id:
      description:
        - The ID of existing scaling rule.
      aliases: [ 'rule_id' ]

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.3.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
- name: basic example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    cooldown: 400
    group_id: asg-2zeimuvzeil1xfuor9ej
    name: ess-rule-foo
    adjustment_type: QuantityChangeInCapacity
    adjustment_value: 3

  tasks:
    - name: launch scaling rule
      ali_ess_rule:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_id: '{{ essgroup.id }}'
        adjustment_type: '{{adjustment_type}}'
        adjustment_value: '{{adjustment_value}}'
        cooldown: '{{cooldown}}'
        name: '{{name}}'

    - name: delete specified scaling rule
      ali_ess_rule:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        name: '{{ name }}'
        state: absent

'''

RETURN = '''
id:
    description: Scaling Rule ID.
    returned: expect absent
    type: str
    sample: "asr-2zefe4bi0jpctd6z726p"
name:
    description: Scaling Rule name.
    returned: expect absent
    type: str
    sample: ess-rule-foo
group_id:
    description: ID of the scaling group of a scaling rule.
    returned: expect absent
    type: str
    sample: "asg-2zeimuvzeil1xfuor9ej"
rule:
    description: The details of a scaling rule.
    returned: expect absent
    type: dict
    sample: {
        "adjustment_type": "QuantityChangeInCapacity", 
        "adjustment_value": 3,
        "ari": "ari:acs:ess:cn-beijing:1204663572767468:scalingrule/asr-2zefe4bi0jpctd6z726p", 
        "cooldown": 400,
        "group_id": "asg-2zegiwc8m3ccxj0y1rbq", 
        "id": "asr-2zefe4bi0jpctd6z726p",
        "name": "from-ansible-roles-test_ess"
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


def get_details(rule):
    return dict(id=rule.id,
                name=rule.name,
                group_id=rule.scaling_group_id,
                ari=rule.ari,
                cooldown=rule.cooldown,
                adjustment_type=rule.adjustment_type,
                adjustment_value=rule.adjustment_value
                )


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(type='str', aliases=['scaling_group_id']),
        adjustment_type=dict(type='str', aliases=['type'], choices=['QuantityChangeInCapacity', 'PercentChangeInCapacity', 'TotalCapacity']),
        adjustment_value=dict(type='int', aliases=['value']),
        name=dict(type='str', aliases=['rule_name']),
        cooldown=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        id=dict(type='str', aliases=['rule_id'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module ali_ess_rule.")

    ess = ess_connect(module)
    state = module.params['state']
    rule_id = module.params['id']
    rule_name = module.params['name']
    scaling_group = module.params['group_id']
    adjustment_type = module.params['adjustment_type']
    adjustment_value = module.params['adjustment_value']
    cooldown = module.params['cooldown']
    changed = False

    current = None
    all_rules = []
    if rule_id or rule_name:
        rules = ess.describe_rules(scaling_group_id=scaling_group, scaling_rule_ids=[rule_id], scaling_rule_names=[rule_name])

        if rules:
            if len(rules) > 1:
                for r in rules:
                    all_rules.append(r.id)
                module.fail_json(msg="There are several scaling rules in our record based on name {0}: {1}. "
                                     "Please specified one using 'id' and try again.".format(rule_name, all_rules))
            current = rules[0]

    if state == 'present':
        if current is None:
            try:
                if not scaling_group:
                    module.exit_json(msg="'group_id': required field when state is present, aborting.")
                if not adjustment_type:
                    module.exit_json(msg="'adjustment_type': required field when state is present, aborting.")
                if not adjustment_value:
                    module.exit_json(msg="'adjustment_value': required field when state is present, aborting.")
                current = ess.create_rule(scaling_group_id=scaling_group, adjustment_type=adjustment_type,
                                          adjustment_value=adjustment_value, name=rule_name, cooldown=cooldown)
                changed = True
            except Exception as e:
                module.fail_json(msg="Create scaling rule got an error: {0}".format(e))

        else:
            try:
                changed = current.modify(adjustment_type=adjustment_type, adjustment_value=adjustment_value,
                                         name=rule_name, cooldown=cooldown)
                if changed:
                    current = current.update(validate=True)
            except Exception as e:
                module.fail_json(msg="Modify scaling rule got an error: {0}".format(e))
        module.exit_json(changed=changed, id=current.id, name=current.name, group_id=current.group_id, rule=get_details(current))

    if current is None:
        if rule_id or rule_name:
                module.fail_json(msg="There are no scaling rule in our record based on id {0} or name {1}. "
                                     "Please check it and try again.".format(rule_id, rule_name))
        module.fail_json(msg='Please specify a scaling rule that you want to terminate by parameters id or name, aborting')

    try:
        module.exit_json(changed=current.terminate())
    except Exception as e:
        module.fail_json(msg='Delete scaling rule {0} got an error: {1}'.format(current.id, e))


if __name__ == '__main__':
    main()

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
module: alicloud_ess_group
version_added: "1.0.9"
short_description: Create or Terminate an scaling group in ESS.
description:
    - A scaling group is a collection of ECS instances with similar configuration deployed in an application scenario.
      It defines the maximum and minimum number of ECS instances in the group,
      associated Server Load Balancer and RDS instances, and other attributes.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix "ali" will be more concise.
  alternative: Use M(ali_ess_group) instead.
options:
    state:
      description:
        - The state of the scaling group after operating.
      default: 'present'
      choices: [ 'present', 'active', 'inactive', 'absent' ]
    name:
      description:
        - Name shown for the scaling group, which must contain 2-40 characters (English or Chinese).
          The name must begin with a number, an upper/lower-case letter or a Chinese character and may contain numbers, "_", "-" or ".".
          Default to scaling group ID.
      aliases: ['group_name' ]
    max_size:
      description:
        - Maximum number of ECS instances in the scaling group. Value range [0, 100].
    min_size:
      description:
        - Minimum number of ECS instances in the scaling group. Value range [0, 100]. Required when C(state=present).
    cooldown:
      description:
        - Default cool-down time (in seconds) of the scaling group. Value range [0, 86400].
      default: 300
      aliases: [ 'default_cooldown' ]
    removal_policies:
      description:
        - Policy for removing ECS instances from the scaling group. Optional values
          OldestInstance(removes the first ECS instance attached to the scaling group); 
          NewestInstance(removes the first ECS instance attached to the scaling group);
          OldestScalingConfiguration(removes the ECS instance with the oldest scaling configuration).
      default: ["OldestScalingConfiguration","OldestInstance"]
      choices: ["OldestScalingConfiguration","NewestInstance","OldestInstance"]
    load_balancer_ids:
      description:
        - ID list of a Server Load Balancer instance. At most 5 Load Balancer instance supported.
      aliases: [ 'lb_ids' ]
    db_instance_ids:
      description:
        - ID list of an RDS instance. At most 8 RDS instance supported.
      aliases: [ 'db_ids' ]
    vswitch_ids:
      description:
        - ID list of a VSwitch. At most 8 vswitch supported.
          The priority of VSwitches descends from 1 to 5, and 1 indicates the highest priority.
      aliases: [ 'subnet_ids' ]
    id:
      description:
        - The ID of existing scaling group.
      aliases: [ 'group_id' ]
    configuration_id:
      description:
        - ID of the active scaling configuration in the scaling group. Required when C(state=active).
      aliases: [ 'scaling_configuration_id' ]

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.3.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# basic provisioning example scaling group
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    ess_group_name: foo
    max_size: 2
    min_size: 0
    cooldown: 400
    removal_policies:
      - 'OldestScalingConfiguration'
      - 'OldestInstance'
    group_id: asg-fh323iwefncew31
    configuration_id: asc-2ze4zleeettwd4sfnrkk

  tasks:
    - name: Create scaling group
      alicloud_ess_group:
        alicloud_region: '{{ alicloud_region }}'
        max_size: '{{ max_size }}'
        min_size: '{{ min_size }}'
        name: '{{ ess_group_name }}'
        vswitch_ids:
          - '{{ subnet.vswitch_id }}'
    
    - name: active a specified scaling group
      alicloud_ess_group:
        alicloud_region: '{{ alicloud_region }}'
        configuration_id: '{{ configuration.id }}'
        id: '{{ group_id }}'
        state: active

'''

RETURN = '''
id:
    description: The ID of existing scaling group.
    returned: expect absent
    type: str
    sample: "asg-2zefe4bi0jpc3tqi8mn8"
name:
    description: The ID of existing scaling group.
    returned: expect absent
    type: str
    sample: "foo"
configuration_id:
    description: ID of the active scaling configuration in the scaling group.
    returned: expect absent
    type: str
    sample: "asc-2ze4zleeettwd4sfnrkk"
group:
    description: The details of a scaling group.
    returned: expect absent
    type: dict
    sample: {
        "configuration_id": asc-2ze4zleeettwd4sfnrkk,
        "cooldown": 300,
        "creation_time": "2018-01-08T05:42Z",
        "db_ids": null,
        "id": "asg-2zefe4bi0jpc3tqi8mn8",
        "load_balancer_id": null,
        "max_size": 2,
        "min_size": 0,
        "name": "foo",
        "status": "active",
        "vswitch_ids": [
            "vsw-2zevfsoh2v7en50w9up6u"
        ],
        "id": "asg-2zefe4bi0jpc3tqi8mn8",
        "name": "foo"
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


def get_details(group):
    result = dict(id=group.id,
                  name=group.name,
                  configuration_id=group.configuration_id,
                  status=group.status,
                  max_size=group.max_size,
                  min_size=group.min_size,
                  load_balancer_id=getattr(group, 'load_balancer_id', None),
                  cooldown=group.cooldown,
                  db_ids=getattr(group, 'db_instance_ids', None),
                  creation_time=group.creation_time
                  )
    vswitch_ids = getattr(group, 'vswitch_ids', None)
    if vswitch_ids:
        result['vswitch_ids'] = vswitch_ids['vswitch_id']

    return result


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        name=dict(type=str, aliases=['group_name']),
        max_size=dict(type=int),
        min_size=dict(type=int),
        state=dict(type=str, default='present', choices=['present', 'active', 'inactive', 'absent']),
        id=dict(type=str, aliases=['group_id']),
        cooldown=dict(type=int, default=300, aliases=['default_cooldown']),
        removal_policies=dict(type=list, default=['OldestScalingConfiguration','OldestInstance']),
        load_balancer_ids=dict(type=list, aliases=['lb_ids']),
        db_instance_ids=dict(type=list, aliases=['db_ids']),
        vswitch_ids=dict(type=list, aliases=['subnet_ids']),
        configuration_id=dict(type=str, aliases=['scaling_configuration_id'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_ess_group.")

    ess = ess_connect(module)
    state = module.params['state']
    group_id = module.params['id']
    group_name = module.params['name']
    max_size = module.params['max_size']
    min_size = module.params['min_size']
    cooldown = module.params['cooldown']
    removal_policies = module.params['removal_policies']
    configuration_id = module.params['configuration_id']

    changed = False

    current = None
    all_groups = []
    if group_id or group_name:
        groups = ess.describe_groups(scaling_group_ids=[group_id], scaling_group_names=[group_name])

        if groups:
            for group in groups:
                all_groups.append(group.id)

            if len(all_groups) > 1:
                module.fail_json(msg="There are several scaling group in our record based on name {0}: {1}. "
                                     "Please specified one using 'id' and try again.".format(group_name, all_groups))

            current = groups[0]

    if state == 'present':
        if current is None:
            try:
                if max_size is None or max_size < 0 or max_size > 100:
                    module.fail_json(msg="'max_size': required field when state is 'present' and its value range [0, 100]. "
                                         "Please check it and try again.")
                if min_size is None or min_size < 0 or min_size > 100:
                    module.fail_json(msg="'min_size': required field when state is 'present' and its value range [0, 100]. "
                                         "Please check it and try again.")
                lb_ids = module.params['load_balancer_ids']
                db_ids = module.params['db_instance_ids']
                vsw_ids = module.params['vswitch_ids']
                if lb_ids and not isinstance(lb_ids, list):
                    module.fail_json(msg="Filed 'load_balancer_ids' should be a list, aborting.")
                if db_ids and not isinstance(db_ids, list):
                    module.fail_json(msg="Filed 'db_instance_ids' should be a list, aborting.")
                if vsw_ids and not isinstance(vsw_ids, list):
                    module.fail_json(msg="Filed 'vswitch_ids' should be a list, aborting.")

                current = ess.create_group(max_size=max_size, min_size=min_size, name=group_name,
                                           default_cooldown=cooldown, removal_policies=removal_policies,
                                           load_balancer_ids=lb_ids, db_instance_ids=db_ids, vswitch_ids=vsw_ids)
                changed = True
            except Exception as e:
                module.fail_json(msg="Create scaling group got an error: {0}".format(e))

        # Modify scaling group attribute
        if group_name != current.name or max_size != current.max_size or min_size != current.min_size \
                or configuration_id != current.configuration_id or cooldown != current.cooldown \
                or removal_policies != current.removal_policies['removal_policy']:
            changed = current.modify(max_size=max_size, min_size=min_size, name=group_name, default_cooldown=cooldown,
                                     removal_policies=removal_policies, scaling_configuration_id=configuration_id)

        module.exit_json(changed=changed, id=current.id, name=current.name, configuration_id=current.configuration_id,
                         group=get_details(current))

    if current is None:
        if group_id or group_name:
            module.fail_json(msg="There are no scaling group in our record based on id {0} or name {1}. "
                                 "Please check it and try again.".format(group_id, group_name))
        module.fail_json(msg='Please specify a scaling group that you want to operate by parameters id or name, aborting')

    if state == 'absent':
        try:
            module.exit_json(changed=current.terminate())
        except Exception as e:
            module.fail_json(msg='Delete scaling group {0} got an error: {1}'.format(current.id, e))

    if state == 'active':
        try:
            if str.lower(current.status) == 'inactive' or current.configuration_id != configuration_id:
                changed = current.enable(scaling_configuration_id=configuration_id)
                current = ess.describe_groups(scaling_group_ids=[group_id])[0]

        except Exception as e:
            module.fail_json(msg='Active scaling group {0} got an error: {1}.'.format(current.id, e))

    elif state == 'inactive':
        try:
            if str.lower(current.status) == 'active':
                changed = current.disable()
                current = ess.describe_groups(scaling_group_ids=[group_id])[0]

        except Exception as e:
            module.fail_json(msg='Inactive scaling group {0} got an error: {1}.'.format(current.id, e))

    module.exit_json(changed=changed, id=current.id, name=current.name, configuration_id=current.configuration_id,
                     group=get_details(current))


if __name__ == '__main__':
    main()

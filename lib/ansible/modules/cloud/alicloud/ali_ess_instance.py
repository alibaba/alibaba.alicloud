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
module: ali_ess_instance
version_added: "1.5.0"
short_description: Add or Remove several ECS instances in ESS
description:
    - Add several ECS instances to a specified scaling group;
      Remove several ECS instances from a specified scaling group.
options:
    state:
      description:
        - present to add ECS instances;
          absent to remove ECS instances.
      default: 'present'
      choices: [ 'present', 'absent' ]
    group_id:
      description:
        - The ID of a scaling group.
      required: True
    instance_ids:
      description:
        - ID list of an ECS instance. At most 20 ECS instance supported. Required when C(state='present').
    creation_type:
      description:
        - ECS instance creation type. Valid when C(state='absent', instance_ids=None).
          'AutoCreated' for the ECS instance is automatically created by the Auto Scaling service in the scaling group.
          'Attached' for the ECS instance is created outside the Auto Scaling service and manually attached to the scaling group.
      choices: [ 'AutoCreated', 'Attached' ]
      default: 'Attached'
      aliases: [ 'type' ]

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.3.0"
notes:
  - If both I(instance_ids) and I(creation_type) are not specified, the module will remove all of ECS instnaces in the
    specified Scaling Group when C(state=absent).
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# basic provisioning example scaling instance
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    instance_ids:
      - "i-2ze2y4x26l66h4b4u884"
      - "i-2ze0eyu760pkh468uwg7"
    group_id: asg-2zebnrbt206pex

  tasks:
    - name: add instances to specified
      ali_ess_instance:
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        group_id: '{{ group_id }}'

    - name: remove auto-created instances
      ali_ess_instance:
        alicloud_region: '{{ alicloud_region }}'
        creation_type: 'AutoCreated'
        group_id: '{{ group_id }}'
        state: absent
    
    - name: remove all of ECS instances
      ali_ess_instance:
        alicloud_region: '{{ alicloud_region }}'
        group_id: '{{ group_id }}'
        state: absent
'''

RETURN = '''
changed:
    description: The result of adding or removing.
    returned: when success
    type: bool
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ess_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(type=str, default='present', choices=['present', 'absent']),
        group_id=dict(type=str, required=True),
        instance_ids=dict(type=list),
        creation_type=dict(type=str, default='Attached', choices=['AutoCreated', 'Attached'], aliases=['type'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module ali_ess_instance.")

    ess = ess_connect(module)
    state = module.params['state']
    group_id = module.params['group_id']
    instance_ids = module.params['instance_ids']
    creation_type = module.params['creation_type']

    if state == 'present' and not instance_ids:
        module.fail_json(msg="Field 'instance_ids' is required when state is 'present'. Aborting.")

    changed = False
    adding = instance_ids
    removing = []
    all = []
    old = ess.describe_instances(scaling_group_id=group_id)
    if old:
        for inst in old:
            if instance_ids:
                if inst.id in instance_ids:
                    adding.remove(inst.id)
                    removing.append(inst.id)
            if state == 'absent' and creation_type and inst.creation_type == creation_type:
                removing.append(inst.id)
            all.append(inst.id)

    if state == 'present':
        if adding:
            try:
                changed = ess.attach_instances(scaling_group_id=group_id, instance_ids=adding)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg="Adding ECS instances to scaling group got an error: {0}.".format(e))

    if not removing:
        removing = all

    if removing:
        try:
            changed = ess.remove_instances(scaling_group_id=group_id, instance_ids=removing)
        except Exception as e:
            module.fail_json(msg='Removing ECS instances from scaling group got an error: {0}.'.format(e))

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()

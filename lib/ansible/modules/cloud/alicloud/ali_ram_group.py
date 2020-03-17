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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_ram_group
version_added: "2.9"
short_description: Create, Delete, Update Ram Groups in Alibaba Cloud.
description:
    - Create, Delete, Update group comments, name in Alibaba Cloud.
    - An unique ali_ram_group module is determined by parameters group_name. 
options:
  state:
    description:
      - If I(state=present), group will be created.
      - If I(state=present), group and new_group_name exists, it will be updated.
      - If I(state=present), group and comments exists, it will be updated.
      - If I(state=present), group and user_name exists, it will add user to group.
      - If I(state=absent), group will be removed.
      - If I(state=absent), group and user_name exists, it will remove user from group.
    choices: ['present', 'absent']
    default: 'present'
    type: str
  user_name:
    description:
      - The username. Required when add user to group or remove user from group.
    type: str
  group_name:
    description:
      - The RAM user group name. It must be 1 to 64 characters in length.
      - This is used to determine if the group already exists.
    aliases: ['name']
    required: True
    type: str
  new_group_name:
    description:
      - The new group name. Required when update group name.
    type: str
  comments:
    description:
      - The comment. It must be 1 to 128 characters in length. Required when update group comments.
    type: str
requirements:
    - "python >= 3.6"
    - "footmark >= 1.17.0"
extends_documentation_fragment:
    - alicloud
author:
    - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Changed. Create a new group
  ali_ram_group:
    group_name: ansible
    comments: create for ansible

- name: Changed. Update group comments
  ali_ram_group:
    group_name: ansible
    comments: just create for ansible

- name: Changed. Update group name
  ali_ram_group:
    group_name: ansible
    new_group_name: ansible1

- name: Changed. Add user to group
  ali_ram_group:
    group_name: ansible1
    user_name: ansible

- name: Changed. Remove user from group
  ali_ram_group:
    group_name: ansible1
    user_name: ansible
    state: absent

- name: Changed. Delete group
  ali_ram_group:
    group_name: ansible1
    state: absent
"""

RETURN = '''
group:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        comments:
            description: The comment.
            returned: always
            type: str
            sample: Development team
        create_date:
            description: The date and time when the RAM user group was created.
            returned: always
            type: str
            sample: 2015-01-23T12:33:18Z
        group_name:
            description: The RAM user group name.
            returned: alway
            type: str
            sample: Dev-Team
        name:
            description: alias of 'group_name'.
            returned: always
            type: str
            sample: Dev-Team
        update_date:
            description: The date and time when a RAM user group was modified.
            returned: always
            type: str
            sample: 2015-01-23T12:33:18Z
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RAMResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def group_exists(module, ram_conn, group_name):
    try:
        for g in ram_conn.list_groups():
            if g.name == group_name:
                return g
        return None
    except Exception as e:
        module.fail_json(msg="Failed to describe Groups: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        group_name=dict(type='str', required=True, aliases=['name']),
        new_group_name=dict(type='str'),
        comments=dict(type='str'),
        user_name=dict(type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module.')

    ram_conn = ram_connect(module)

    # Get values of variable
    state = module.params['state']
    group_name = module.params['group_name']
    new_group_name = module.params['new_group_name']
    comments = module.params['comments']
    user_name = module.params['user_name']
    changed = False

    # Check if user exists
    group = group_exists(module, ram_conn, group_name)

    if state == 'absent':
        if user_name:
            try:
                changed = group.remove_user(user_name=user_name)
                module.exit_json(changed=changed, group=group.read())
            except Exception as e:
                module.fail_json(msg='Unable to remove user to group {0}, error: {1}'.format(group_name, e))
        if not group:
            module.exit_json(changed=changed, group={})
        try:
            module.exit_json(changed=group.delete(), group={})
        except RAMResponseError as ex:
            module.fail_json(msg='Unable to delete group {0}, error: {1}'.format(group_name, ex))

    if not group:
        try:
            group = ram_conn.create_group(**module.params)
            module.exit_json(changed=True, group=group.read())
        except RAMResponseError as e:
            module.fail_json(msg='Unable to create group, error: {0}'.format(e))

    if user_name:
        try:
            changed = group.add_user(user_name=user_name)
        except Exception as e:
            module.fail_json(msg='Unable to add user to group {0}, error: {1}'.format(group_name, e))

    if comments or new_group_name:
        try:
            changed = group.update(comments=comments, new_group_name=new_group_name)
        except RAMResponseError as e:
            module.fail_json(msg='Unable to update comments, error: {0}'.format(e))

    module.exit_json(changed=changed, group=group.read())


if __name__ == '__main__':
    main()

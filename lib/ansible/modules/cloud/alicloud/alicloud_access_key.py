#!/usr/bin/python
# coding=utf-8
# Copyright (c) 2017 Alibaba Group Holding Limited. Zhuwei <rockzhu3344@sina.com>
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

from __future__ import absolute_import, division, print_function
metaclass = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_access_key
short_description: ansible can manage aliyun access_key through this module 
version_added: "2.6"
description:
    - This module allows the user to manage access-keys. Includes those commands:'present', 'absent'
options:
  state:
    description:
      -  Create,delete or update the access_key of the user. 
    choices: [ 'present', 'absent']
  user_name:
    description:
      - The user name. A name is created from the specified user.
    required: true
    aliases: [ 'name' ]
  access_key_id：
    description:
      - The symbol to identity the access_key.
  is_active:
    description:
      - The access_key's status can be True or False.
    type: bool
    default: 'True'
extends_documentation_fragment:
    - alicloud
author:
    - Zhu Wei (@zhuweif)
'''

EXAMPLES = '''
#
# AccessKey Management
#

# basic provisioning example to manage access_key
- name: basic provisioning example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing

  tasks:
    - name: create access_key
      alicloud_ram_access_key:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name: '{{ user_name }}'
        state: 'present'
      register: result
    - debug: var=result

    - name: delete access_key
      alicloud_ram_access_key:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        access_key_ids:'{{ access_key_ids }}'
        state: 'absent'
      register: result
    - debug: var=result
'''

RETURN = '''
access_key:
    description: the access_key's headers after create access_key
    returned: on present
    type: dict
    sample: {
        "access_key_id": "abc12345",
        "access_key_secret": "abc12345",
        "status": "Active",
        "create_status": "2015-01-23T12:33:18Z"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec,ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False

def ali_access_key_create(module,ram):
    #user_name
    required_vars = ['user_name']
    valid_vars = ['access_key_id','is_active']
    params=validate_parameters(required_vars, valid_vars, module)
    changed = False
    try:
        if params['access_key_id']:
            changed=ram.update_access_key(user_name=module.params.get('user_name'), access_key_id=params['access_key_id'],is_active=params['is_active'])
            module.exit_json(changed=changed)
        else:
            result = ram.create_access_key(user_name=module.params.get('user_name'))
            module.exit_json(changed=changed, msg=result)
    except Exception as e:
        module.fail_json(msg="Create or update access_key got an error: {0}".format(e))

def ali_access_key_del(module,ram):
    required_vars = ['user_name','access_key_id']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    changed = False
    try:
        changed=ram.delete_access_key(user_name=module.params.get('user_name'),access_key_id=module.params.get('access_key_id'))
    except Exception as e:
        module.fail_json(msg="Failed to delete access_key {0} with error {1}".format(module.params.get('access_key_id'),e))
    module.exit_json(changed=changed)

def validate_parameters(required_vars, valid_vars, module):
    state = module.params.get('state')
    for v in required_vars:
        if not module.params.get(v):
            module.fail_json(msg="Parameter %s required for %s state" % (v, state))
    optional_params = {
        'access_key_id' : 'access_key_id',
        'is_active' : 'is_active'
    }

    params = {}
    for (k, v) in optional_params.items():
        if module.params.get(k) is not None and k not in required_vars:
            if k in valid_vars:
                params[v] = module.params[k]
            else:
                if module.params.get(k) is False:
                    pass
                else:
                    module.fail_json(msg="Parameter {0} is not valid for {1} command".format(k, state))
    return params

def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['present', 'absent'],required=True),
        user_name = dict(required=True),
        access_key_id = dict(required=False),
        is_active = dict(default=True, required=False),
    ))
    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_access_key.")
    invocations = {
        'present': ali_access_key_create,
        'absent': ali_access_key_del,
    }
    module = AnsibleModule(argument_spec=argument_spec)
    ram = ram_connect(module)
    invocations[module.params.get('state')](module, ram)

if __name__ == '__main__':
    main()

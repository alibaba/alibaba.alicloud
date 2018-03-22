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


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_ram_access_key
short_description: ansible can manage aliyun access_key through this module 
version_added: "2.5"
description:
    - "This module allows the user to manage access-keys. Includes those commands:'present', 'list', 'absent'
options:
  state:
    description:
      - 'present', 'list', 'absent' access_key
    choices: [ 'present','list','absent']
  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]
  access_key_id：
    description:
      - The symbol to identity the access_key.
  is_active:
    description:
      - The access_key's status can be 'Active' or 'Inactive'.
extends_documentation_fragment:
    - alicloud
author:
    - Zhe Wei (@zhuweif)

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
        user_name:'{{ user_name }}'
        access_key_ids:'{{  }}'
        is_active:'{{ True or False }}'
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
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ram import ram_argument_spec,ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False

def ali_access_key_create(module, ram):
    #user_name
    required_vars = ['user_name']
    valid_vars = ['access_key_ids','is_active']
    params=validate_parameters(required_vars, valid_vars, module)
    changed = False
    try:
        result=ram.create_access_key(user_name=module.params.get('user_name'), access_key_ids=params['access_key_ids'],is_active=params['is_active'])
        if result:
            changed=True
    except Exception as e:
        module.fail_json(msg="Create or update access_key got an error: {0}".format(e))
    module.exit_json(changed=changed, msg=result)

def ali_access_key_del(module,ram):
    required_vars = ['user_name','access_key_ids']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    changed = False
    try:
         result=ram.delete_access_keys(user_name=module.params.get('user_name'),access_key_ids=module.params.get('access_key_ids'))
         module.exit_json(changed=True, msg=result)
    except Exception as e:
        module.fail_json(msg="Failed to delete access_key {0}with error {1}".format(module.params.get('access_key_ids'),e))
    module.exit_json(changed=changed, msg=result)

def validate_parameters(required_vars, valid_vars, module):
    state = module.params.get('state')
    for v in required_vars:
        if not module.params.get(v):
            module.fail_json(msg="Parameter %s required for %s state" % (v, state))
    optional_params = {
        'access_key_ids' : 'access_key_ids',
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
                    module.fail_json(msg="Parameter %s is not valid for %s command" % (k, state))
    return params


def main():
    argument_spec = ram_argument_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['present', 'absent'],required=True),
        user_name = dict(required=True),
        access_key_ids = dict(required=False),
        is_active = dict(required=False),
    ))
    invocations = {
        'present': ali_access_key_create,
         'absent': ali_access_key_del,
    }
    module = AnsibleModule(argument_spec=argument_spec)
    ram = ram_connect(module);
    invocations[module.params.get('state')](module, ram)


if __name__ == '__main__':
    main()

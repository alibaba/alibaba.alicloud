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


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: alicloud_ram_access_key

short_description: ansible can manage aliyun access_key through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage access-keys. Includes those commands:'create', 'list', 'delete', 'update'"

options:
  state:
    description:
      - 'create', 'list', 'delete', 'update' access_key
    choices: [ 'create', 'list', 'delete', 'update' ]

  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters

  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]

  access_key_id：
    description:
      - The symbol to identity the access_key.

  status:
    description:
      - The access_key's status can be 'Active' or 'Inactive'.

extends_documentation_fragment:
    - 

author:
    - Your Name (@zhuweif)

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
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-bejing

  tasks:
    - name: create access_key
      alicloud_ram_access_key:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'create'
      register: result
    - debug: var=result

    - name: list access_keys
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'list'
      register: result
    - debug: var=result

    - name: update access_key'status
      alicloud_ram_access_key:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        access_key_id:'{{ access_key_id }}'
        status:'{{ Active or Inactive }}'
        state: 'update'
      register: result
    - debug: var=result

    - name: delete access_key
      alicloud_ram_access_key:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        access_key_id:'{{ access_key_id }}'
        state: 'delete'
      register: result
    - debug: var=result
'''

import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import *
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import ListAccessKeysRequest,CreateAccessKeyRequest,UpdateAccessKeyRequest,DeleteAccessKeyRequest

result = dict(
    success=False,
    original_message='',
    message=''
)


def ali_connection_spec():
    return dict(
        alicloud_secret_key=dict(aliases=['secret_key'], required=True, no_log=True),
        alicloud_access_key=dict(aliases=['access_key'], required=True, no_log=True),
        alicloud_region=dict(aliases=['region_id'], required=True, no_log=True)
    )

def validate_parameters(required_vars, valid_vars, module):
    state = module.params.get('state')
    for v in required_vars:
        if not module.params.get(v):
            module.fail_json(msg="Parameter %s required for %s state" % (v, command))
    optional_params = {
        'access_key_id' : 'access_key_id',
        'status' : 'status'
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
                    module.fail_json(msg="Parameter %s is not valid for %s command" % (k, command))
    return params


def get_ali_connection_info(module):
    # Check module args for credentials, then check environment vars
    # access_key
    access_key = module.params.get('alicloud_access_key')
    secret_key = module.params.get('alicloud_secret_key')
    region = module.params.get('alicloud_region')

    if not access_key:
        if os.environ.get('ALICLOUD_ACCESS_KEY_ID'):
            access_key = os.environ['ALICLOUD_ACCESS_KEY_ID']
        elif os.environ.get('ALICLOUD_ACCESS_KEY'):
            access_key = os.environ['ALICLOUD_ACCESS_KEY']
        else:
            # in case access_key came in as empty string
            access_key = None

    if not secret_key:
        if os.environ.get('ALICLOUD_SECRET_ACCESS_KEY'):
            secret_key = os.environ['ALICLOUD_SECRET_ACCESS_KEY']
        elif os.environ.get('ALICLOUD_SECRET_KEY'):
            secret_key = os.environ['ALICLOUD_SECRET_KEY']
        else:
            # in case secret_key came in as empty string
            secret_key = None

    if not region:
        if 'ALICLOUD_REGION' in os.environ:
            region = os.environ['CLOUD_REGION']
        elif 'ALICLOUD_DEFAULT_REGION' in os.environ:
            region = os.environ['ALICLOUD_DEFAULT_REGION']
        else:
            region = None

    return access_key, secret_key, region


def ali_access_key_list(module,clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    list_access_keys_req = ListAccessKeysRequest.ListAccessKeysRequest()
    list_access_keys_req.set_UserName(module.params.get('user_name'))
    list_access_keys_req.set_accept_format('json')

    try:
        result = clt.do_action_with_exception(list_access_keys_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list access_keys: " % e.message)


def ali_access_key_add(module, clt):
    #user_name
    required_vars = ['user_name']
    valid_vars = ['']
    params=validate_parameters(required_vars, valid_vars, module)
    access_key_add_req = CreateAccessKeyRequest.CreateAccessKeyRequest()
    access_key_add_req.set_UserName(module.params.get('user_name'))

    changed = False
    access_key_add_result=None
    try:
        access_key_add_result = clt.do_action_with_exception(access_key_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to add access_key: %s" % e.message)

    module.exit_json(changed=changed, msg=access_key_add_result)


def ali_access_key_update(module,clt):
    #ser_name, access_key_id, status
    required_vars = ['user_name','access_key_id','status']
    valid_vars = ['']
    params=validate_parameters(required_vars, valid_vars, module)
    access_key_update_req = UpdateAccessKeyRequest.UpdateAccessKeyRequest()
    access_key_update_req.set_UserName(module.params.get('user_name'))
    access_key_update_req.set_UserAccessKeyId(module.params.get('access_key_id'))
    access_key_update_req.set_Status(module.params.get('status'))
    access_key_update_req.set_accept_format('json')
    changed = False
    access_key_update_result=None
    try:
        access_key_update_result = clt.do_action_with_exception(access_key_update_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to update access_key: %s" % e.message)

    module.exit_json(changed=changed, msg=access_key_update_result)


def ali_access_key_del(module,clt):
    required_vars = ['user_name','access_key_id']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    access_key_del_req = DeleteAccessKeyRequest.DeleteAccessKeyRequest()
    access_key_del_req.set_UserName(module.params.get('user_name'))
    access_key_del_req.set_UserAccessKeyId(module.params.get('access_key_id'))
    access_key_del_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(access_key_del_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete access_key: %s" % e.message)


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'list',  'delete', 'update'],required=True),
        user_name = dict(required=True),
        access_key_id = dict(required=False),
        status = dict(required=False),
    ))
    invocations = {
        'create': ali_access_key_add,
        'delete': ali_access_key_del,
        'list': ali_access_key_list,
        'update': ali_access_key_update,
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode = True
    )

    ak, secret_key, region_id = get_ali_connection_info(module)

    if not ak:
        module.fail_json(msg="Accesskey not specified. Unable connect to AliYun.")
    if not secret_key:
        module.fail_json(msg="Secretkey not specified. Unable connect to AliYun.")
    if not region_id:
        module.fail_json(msg="Region not specified. Unable connect to AliYun.")

    clt = client.AcsClient(ak, secret_key, region_id)

    invocations[module.params.get('state')](module, clt)


if __name__ == '__main__':
    main()

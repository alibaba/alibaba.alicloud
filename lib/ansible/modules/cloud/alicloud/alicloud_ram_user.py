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
module: alicloud_ram_user

short_description: ansible can manage aliyun users through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage ram-users. Includes those commands:'create', 'list', 'get',  'delete', 'update'"

options:
  state:
    description:
      - 'create', 'list', 'get',  'delete', 'update' user
    choices: [ 'create', 'list', 'get',  'delete', 'update' ]
    
  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters
    
  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]
    
  phone:
  email：
    description:
      - The user info.
      
  comments:
    description:
      - The description of the user, with a length limit of [0, 256] characters.
        Leaving it blank means null, which is the default value.
        
  new_user_name:
  new_phone:
  new_email：
  new_coments:
    description:
      - When update user info,those user's properties can be setted.

extends_documentation_fragment:
    - 

author:
    - Your Name (@zhuweif)

'''

EXAMPLES = '''
#
# User Management
#

# basic provisioning example to manage user
- name: basic provisioning example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-bejing
    
  tasks:
    - name: create user
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        display_name:'{{ display_name }}'
        phone:'{{ phone }}'
        email:'{{ email }}'
        state: 'create'
      register: result
    - debug: var=result
    
    - name: list user
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'list'
      register: result
    - debug: var=result

    - name: get user
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'get'
      register: result
    - debug: var=result
    
    - name: update user
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        new_user_name:'{{ new_user_name }}'
        new_email:'{{ new_email }}'
        new_comments:'{{ new_comments }}'
        state: 'update'
      register: result
    - debug: var=result
    
    - name: delete user
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'delete'
      register: result
    - debug: var=result
    
    - name: change child account password
      alicloud_ram_user:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        old_pwd:'{{ old_pwd }}'
        new_pwd:'{{ new_pwd }}'
        state: 'changePwd'
      register: result
    - debug: var=result
'''

import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import ListUsersRequest, CreateUserRequest, GetUserRequest, UpdateUserRequest, \
    DeleteUserRequest, ChangePasswordRequest


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
            module.fail_json(msg="Parameter %s required for %s state" % (v, state))
    optional_params = {
        'comments': 'comments',
        'new_user_name': 'new_user_name',
        'new_phone': 'new_phone',
        'new_email': 'new_email',
        'new_comments': 'new_comments',
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
                    module.fail_json(msg="Parameter %s is not valid for %s state" % (k, state))
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


def ali_user_list(module, clt):
    user_list_req = ListUsersRequest.ListUsersRequest()
    user_list_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(user_list_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list user: " % e.message)


def ali_user_add(module, clt):
    # user_name, display_name, phone, email, comments
    required_vars = ['user_name', 'display_name', 'phone', 'email']
    valid_vars = ['comments']
    params = validate_parameters(required_vars, valid_vars, module)
    user_add_req = CreateUserRequest.CreateUserRequest()
    user_add_req.set_UserName(module.params.get('user_name'))
    user_add_req.set_DisplayName(module.params.get('display_name'))
    user_add_req.set_MobilePhone(module.params.get('phone'))
    user_add_req.set_Email(module.params.get('email'))
    if 'comments' in params:
        user_add_req.set_Comments(params['comments'])
    user_add_req.set_accept_format('json')

    changed = False
    user_add_result = None
    try:
        user_add_result = clt.do_action_with_exception(user_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to create user: %s" % e.message)

    module.exit_json(changed=changed, msg=user_add_result)


def ali_user_get(module, clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    user_get_req = GetUserRequest.GetUserRequest()
    user_get_req.set_UserName(module.params.get('user_name'))
    user_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(user_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get user: %s" % e.message)


def ali_user_update(module, clt):
    required_vars = ['user_name']
    valid_vars = ['new_user_name', 'new_phone', 'new_email', 'new_comments']
    params = validate_parameters(required_vars, valid_vars, module)
    user_update_req = UpdateUserRequest.UpdateUserRequest()
    user_update_req.set_UserName(module.params.get('user_name'))
    user_update_req.set_accept_format('json')
    if 'new_user_name' in params:
        user_update_req.set_NewUserName(params['new_user_name'])
    else:
        user_update_req.set_NewUserName(module.params.get('user_name'))
    if 'new_phone' in params:
        user_update_req.set_NewMobilePhone(params['new_phone'])
    if 'new_email' in params:
        user_update_req.set_NewEmail(params['new_email'])
    if 'new_comments' in params:
        user_update_req.set_NewComments(params['new_comments'])
    changed = False
    user_update_result = None
    try:
        user_update_result = clt.do_action_with_exception(user_update_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to update user: %s" % e.message)

    module.exit_json(changed=changed, msg=user_update_result)


def ali_user_del(module, clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    user_del_req = DeleteUserRequest.DeleteUserRequest()
    user_del_req.set_UserName(module.params.get('user_name'))
    user_del_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(user_del_req)
        module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete user: %s" % e.message)


def ali_user_child_change_pwd(module, clt):
    # pwd, new_pwd
    required_vars = ['old_pwd', 'new_pwd']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    change_pwd_req = ChangePasswordRequest.ChangePasswordRequest()
    change_pwd_req.set_OldPassword(module.params.get('old_pwd'))
    change_pwd_req.set_NewPassword(module.params.get('new_pwd'))
    change_pwd_req.set_accept_format('json')
    changed = False
    user_child_change_pwd_result = None
    try:
        user_child_change_pwd_result = clt.do_action_with_exception(change_pwd_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to change childAccount password: %s" % e.message)

    module.exit_json(changed=changed, msg=user_child_change_pwd_result)


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'list', 'get', 'delete', 'update'], required=True),
        user_name=dict(aliases=['name'], required=False),
        display_name=dict(required=False),
        phone=dict(required=False),
        email=dict(required=False),
        comments=dict(required=False),
        new_user_name=dict(required=False),
        new_phone=dict(required=False),
        new_email=dict(required=False),
        new_comments=dict(required=False),
    ))
    invocations = {
        'create': ali_user_add,
        'delete': ali_user_del,
        'get': ali_user_get,
        'list': ali_user_list,
        'update': ali_user_update,
        'changePwd': ali_user_child_change_pwd
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
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

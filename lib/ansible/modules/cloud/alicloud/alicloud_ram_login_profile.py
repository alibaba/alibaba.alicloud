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
module: alicloud_ram_login_profile

short_description: ansible can manage aliyun login_profile through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage login_profiles. Includes those commands:'create', 'get',  'delete', 'update'"

options:
  state:
    description:
      - 'create', 'get',  'delete', 'update' login_profile
    choices: [ 'create', 'get',  'delete', 'update' ]

  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters

  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]

  pwd：
    description:
      - The login password.

  pwd_reset_req:
    description:
      - Whether allow user to reset the password 'True' or 'False'.

  mfa_req:
    description:
      - Whether allow user to use mfa device 'True' or 'False'.

  new_pwd:
  new_pwd_reset_req：
  new_new_mfa_req:
    description:
      - When update login_profile info,those  properties can be setted.

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
    - name: create login_profile
      alicloud_ram_login_profile:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        pwd:'{{ pwd }}'
        pwd_reset_req:'{{ True or False }}'
        mfa_req:'{{ True or False }}'
        state: 'create'
      register: result
    - debug: var=result

    - name: get login_profile
      alicloud_ram_login_profile:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'get'
      register: result
    - debug: var=result

    - name: update login_file
      alicloud_ram_login_profile:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        new_pwd:'{{ new_pwd }}'
        new_pwd_reset_req:'{{  True or False  }}'
        new_mfa_req:'{{  True or False  }}'
        state: 'update'
      register: result
    - debug: var=result

    - name: delete login_file
      alicloud_ram_login_profile:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'delete'
      register: result
    - debug: var=result
'''

import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import CreateLoginProfileRequest,GetLoginProfileRequest,DeleteLoginProfileRequest,UpdateLoginProfileRequest


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
        'pwd': 'pwd',
        'new_pwd': 'new_pwd',
        'new_pwd_reset_req': 'new_pwd_reset_req',
        'new_mfa_req': 'new_mfa_req',
        'pwd_reset_req': 'pwd_reset_req',
        'mfa_req': 'mfa_req'
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


def ali_login_profile_add(module, clt):
    #user_name, pwd, pwd_reset_req, mfa_req
    required_vars = ['user_name', 'pwd']
    valid_vars = ['pwd_reset_req','mfa_req']
    params=validate_parameters(required_vars, valid_vars, module)
    login_profile_add_req = CreateLoginProfileRequest.CreateLoginProfileRequest()
    login_profile_add_req.set_UserName(module.params.get('user_name'))
    login_profile_add_req.set_Password(module.params.get('pwd'))
    login_profile_add_req.set_accept_format('json')
    if 'pwd_reset_req' in params:
        login_profile_add_req.set_PasswordResetRequired(params['pwd_reset_req'])
    else:
        login_profile_add_req.set_PasswordResetRequired(False)
    if 'mfa_req' in params:
        login_profile_add_req.set_MFABindRequired(params['mfa_req'])
    else:
        login_profile_add_req.set_MFABindRequired(False)

    changed = False
    login_profile_add_result=None
    try:
        login_profile_add_result = clt.do_action_with_exception(login_profile_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to create user: %s" % e.message)

    module.exit_json(changed=changed, msg=login_profile_add_result)


def ali_login_profile_get(module,clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    login_profile_get_req = GetLoginProfileRequest.GetLoginProfileRequest()
    login_profile_get_req.set_UserName(module.params.get('user_name'))
    login_profile_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(login_profile_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get login_profile: %s" % e.message)


def ali_login_profile_update(module,clt):
    #user_name, new_pwd, new_pwd_reset_req,new_mfa_req
    required_vars = ['user_name']
    valid_vars = ['new_pwd', 'new_pwd_reset_req', 'new_mfa_req']
    params=validate_parameters(required_vars, valid_vars, module)
    login_profile_update_req = UpdateLoginProfileRequest.UpdateLoginProfileRequest()
    login_profile_update_req.set_UserName(module.params.get('user_name'))
    login_profile_update_req.set_accept_format('json')
    if 'new_pwd' in params:
        login_profile_update_req.set_Password(params['new_pwd'])
    if 'new_pwd_reset_req' in params:
        login_profile_update_req.set_PasswordResetRequired(params['new_pwd_reset_req'])
    if 'new_mfa_req' in params:
        login_profile_update_req.set_MFABindRequired(params['new_mfa_req'])
    changed = False
    login_profile_update_result=None
    try:
        login_profile_update_result = clt.do_action_with_exception(login_profile_update_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to update login_profile: %s" % e.message)

    module.exit_json(changed=changed, msg=login_profile_update_result)


def ali_login_profile_del(module,clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    login_profile_del_req = DeleteLoginProfileRequest.DeleteLoginProfileRequest()
    login_profile_del_req.set_UserName(module.params.get('user_name'))
    login_profile_del_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(login_profile_del_req)
        module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete user: %s" % e.message)
        return None


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'get',  'delete', 'update'],required=True),
        user_name = dict(required=True),
        pwd = dict(required=False),
        new_pwd = dict(required=False),
        new_pwd_reset_req = dict(required=False),
        new_mfa_req = dict(required=False),
        pwd_reset_req = dict(required=False),
        mfa_req = dict(required=False),
    ))
    invocations = {
        'create': ali_login_profile_add,
        'delete': ali_login_profile_del,
        'get': ali_login_profile_get,
        'update': ali_login_profile_update,
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

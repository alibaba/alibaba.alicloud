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
module: alicloud_ram_security_setting

short_description: ansible can manage aliyun ram_security_settings through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage ram_security_settings. Includes those commands:'set_alias', 'get_alias',  'clear_alias', 'set_pwd_policy', 'get_pwd_policy', 'set_security_preference'"

options:
  state:
    description:
      - 'set_alias', 'get_alias',  'clear_alias', 'set_pwd_policy', 'get_pwd_policy', 'set_security_preference'
    choices: ['set_alias', 'get_alias',  'clear_alias', 'set_pwd_policy', 'get_pwd_policy', 'set_security_preference']

  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters

  alias_name：
    description:
      - The alias name for account.

  min_len:
    description:
      - The minimum length of the password.

  lowercase_requirable:
    description:
      - The lowercase-letter will be needed in passsword: True or False.
      
  uppercase_requiable:
    description:
      - The uppercase-letter will be needed in password: True or False.
      
  num_requirable:
    description:
      - The numbers will be needed in password: True or False.

  symbols_requirable:
    description:
      - The special symbol will be needed in password: True or False.
      
  save_mfa_ticket_enable:
    description:
      - The MFA key can be save in one week: True or False.
      
  change_pwd_enable:
    description:
      - Allow user to change password: True or False.

  manage_access_key_enable:
    description:
      - Allow user to manage the access keys: True or False.
      
  manage_mfa_enable:
    description:
      - Allow user to manage the mfa devices: True or False.

extends_documentation_fragment:
    - 

author:
    - Your Name (@zhuweif)

'''

EXAMPLES = '''
#
# Mfa Management
#

# basic provisioning example to manage mfa
- name: basic provisioning example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-bejing

  tasks:
    - name: set alias-name for user-account
      alicloud_ram_security_setting:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alias_name:'{{ alias_name }}'
        state: 'set_alias'
      register: result
    - debug: var=result

    - name: get alias-name of user-account
      alicloud_ram_security_setting:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'get_alias'
      register: result
    - debug: var=result

    - name: clear alias-name of user-account
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'clear_alias'
      register: result
    - debug: var=result

    - name: set password policy of child account
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        min_len:'{{ min_len }}'
        lowercase_requirable:'{{ serial_num }}'
        uppercase_requiable: 'True or False'
        num_requirable: 'True or False'
        symbols_requirable: 'True or False'
        state: 'set_pwd_policy'
      register: result
    - debug: var=result

    - name: get password policy of child account
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'get_pwd_policy'
      register: result
    - debug: var=result
    
    - name: set security_preference
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        save_mfa_ticket_enable: 'True or False'
        change_pwd_enable: 'True or False'
        manage_access_key_enable: 'True or False'
        manage_mfa_enable: 'True or False'
        state: 'set_security_preference'
      register: result
    - debug: var=result
'''

import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import SetAccountAliasRequest,GetAccountAliasRequest,SetPasswordPolicyRequest,GetPasswordPolicyRequest,ClearAccountAliasRequest,SetSecurityPreferenceRequest

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
            module.fail_json(msg="Parameter %s required for %s state" % (v, state))
    optional_params = {
        'alias_name' : 'alias_name',
        'new_role_policy' : 'new_role_policy',
        'min_len': 'min_len',
        'lowercase_requirable': 'lowercase_requirable',
        'uppercase_requiable': 'uppercase_requiable',
        'num_requirable': 'num_requirable',
        'symbols_requirable': 'symbols_requirable',
        'save_mfa_ticket_enable' : 'save_mfa_ticket_enable',
        'change_pwd_enable': 'change_pwd_enable',
        'manage_access_key_enable': 'manage_access_key_enable',
        'manage_mfa_enable': 'manage_mfa_enable',
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


def ali_alias_add(module,clt):
    #alias_name
    required_vars = ['alias_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    alias_add_req = SetAccountAliasRequest.SetAccountAliasRequest()
    alias_add_req.set_AccountAlias(module.params.get('alias_name'))
    alias_add_req.set_accept_format('json')
    changed = False
    alias_add_result=None
    try:
        alias_add_result = clt.do_action_with_exception(alias_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to add alias: %s" % e.message)

    module.exit_json(changed=changed, msg=alias_add_result)


def ali_alias_get(module,clt):
    alias_get_req = GetAccountAliasRequest.GetAccountAliasRequest()
    alias_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(alias_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get alias: %s" % e.message)


def ali_alias_del(module,clt):
    alias_del_req = ClearAccountAliasRequest.ClearAccountAliasRequest()
    alias_del_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(alias_del_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete alias: %s" % e.message)


def ali_pwd_policy_add(module,clt):
    #alias_name
    required_vars = ['']
    valid_vars = ['min_len', 'lowercase_requirable', 'uppercase_requiable', 'num_requirable', 'symbols_requirable']
    params=validate_parameters(required_vars, valid_vars, module)
    pwd_policy_add_req = SetPasswordPolicyRequest.SetPasswordPolicyRequest()
    if 'min_len' in params:
        pwd_policy_add_req.set_MinimumPasswordLength(params['min_len'])
    if 'lowercase_requirable' in params:
        pwd_policy_add_req.set_RequireLowercaseCharacters(params['lowercase_requirable'])
    if 'uppercase_requiable' in params:
        pwd_policy_add_req.set_RequireUppercaseCharacters(params['uppercase_requiable'])
    if 'num_requirable' in params:
        pwd_policy_add_req.set_RequireNumbers(params['num_requirable'])
    if 'symbols_requirable' in params:
        pwd_policy_add_req.set_RequireSymbols(params['symbols_requirable'])
    pwd_policy_add_req.set_accept_format('json')
    changed = False
    pwd_policy_add_result=None
    try:
        pwd_policy_add_result = clt.do_action_with_exception(pwd_policy_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to add password policy: %s" % e.message)

    module.exit_json(changed=changed, msg= pwd_policy_add_result)


def ali_pwd_policy_get(module,clt):
    pwd_policy_get_req = GetPasswordPolicyRequest.GetPasswordPolicyRequest()
    pwd_policy_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(pwd_policy_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get password policy: %s" % e.message)


def ali_security_preference_add(module,clt):
    #'save_mfa_ticket_enable', 'change_pwd_enable', 'manage_access_key_enable', 'manage_mfa_enable'
    required_vars = ['']
    valid_vars = ['save_mfa_ticket_enable', 'change_pwd_enable', 'manage_access_key_enable', 'manage_mfa_enable']
    params=validate_parameters(required_vars, valid_vars, module)
    security_preference_set_req = SetSecurityPreferenceRequest.SetSecurityPreferenceRequest()
    if 'save_mfa_ticket_enable' in params:
        security_preference_set_req.set_EnableSaveMFATicket(params['save_mfa_ticket_enable'])
    if 'change_pwd_enable' in params:
        security_preference_set_req.set_AllowUserToChangePassword(params['change_pwd_enable'])
    if 'manage_access_key_enable' in params:
        security_preference_set_req.set_AllowUserToManageAccessKeys(params['manage_access_key_enable'])
    if 'manage_mfa_enable' in params:
        security_preference_set_req.set_AllowUserToManageMFADevices(params['manage_mfa_enable'])
    security_preference_set_req.set_accept_format('json')
    changed = False
    security_preference_set_result=None
    try:
        security_preference_set_result = clt.do_action_with_exception(security_preference_set_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to security preference : %s" % e.message)

    module.exit_json(changed=changed, msg=security_preference_set_result)


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['set_alias', 'get_alias',  'clear_alias', 'set_pwd_policy', 'get_pwd_policy', 'set_security_preference'],required=True),
        alias_name = dict(required=False),
        min_len = dict(required=False),
        lowercase_requirable = dict(required=False),
        uppercase_requiable= dict(required=False),
        num_requirable=dict(required=False),
        symbols_requirable=dict(required=False),
        save_mfa_ticket_enable=dict(required=False),
        change_pwd_enable=dict(required=False),
        manage_access_key_enable=dict(required=False),
        manage_mfa_enable=dict(required=False),
    ))
    invocations = {
        'set_alias': ali_alias_add,
        'get_alias': ali_alias_get,
        'clear_alias': ali_alias_del,
        'set_pwd_policy': ali_pwd_policy_add,
        'get_pwd_policy': ali_pwd_policy_get,
        'set_security_preference': ali_security_preference_add,
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

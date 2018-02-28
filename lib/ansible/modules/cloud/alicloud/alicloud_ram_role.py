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
module: alicloud_ram_role

short_description: ansible can manage aliyun role through this module 

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

  role_name:
    description:
      - The role name. A name is created from the specified role.
    aliases: [ 'name' ]

  role_policy:
    description:
      - The authority policy of the role.

  description:
    description:
      - The description of the role, with a length limit of [0, 256] characters.
        Leaving it blank means null, which is the default value.

  new_role_policy:
    description:
      - When update role info,the authority policy can be setted.

extends_documentation_fragment:
    - 

author:
    - Your Name (@zhuweif)

'''

EXAMPLES = '''
#
# Role Management
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
    - name: create role
      alicloud_ram_role:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        role_name:'{{ role_name }}'
        role_policy:'{{ role_policy }}'
        state: 'create'
      register: result
    - debug: var=result

    - name: list role
      alicloud_ram_role:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'list'
      register: result
    - debug: var=result

    - name: get role
      alicloud_ram_role:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        role_name:'{{ role_name }}'
        state: 'get'
      register: result
    - debug: var=result

    - name: update role
      alicloud_ram_role:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        role_name:'{{ role_name }}'
        new_role_policy:'{{ new_role_policy }}'
        state: 'update'
      register: result
    - debug: var=result

    - name: delete role
      alicloud_ram_role:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        role_name:'{{ role_name }}'
        state: 'delete'
      register: result
    - debug: var=result
'''

import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import ListRolesRequest,GetRoleRequest,CreateRoleRequest,UpdateRoleRequest,DeleteRoleRequest


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
        'description' : 'description',
        'new_role_policy' : 'new_role_policy'
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


def ali_role_list(module,clt):
    list_roles_req = ListRolesRequest.ListRolesRequest()
    list_roles_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(list_roles_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list roles: " % e.message)


def ali_role_get(module,clt):
    #role_name
    required_vars = ['role_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    role_get_req = GetRoleRequest.GetRoleRequest()
    role_get_req.set_RoleName(module.params.get('role_name'))
    role_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(role_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get role: %s" % e.message)


def ali_role_add(module, clt):
    #role_name role_policy description
    required_vars = ['role_name','role_policy']
    valid_vars = ['description']
    params=validate_parameters(required_vars, valid_vars, module)
    role_add_req = CreateRoleRequest.CreateRoleRequest()
    role_add_req.set_RoleName(module.params.get('role_name'))
    role_add_req.set_AssumeRolePolicyDocument(module.params.get('role_policy'))
    role_add_req.set_accept_format('json')
    if 'description' in params:
        role_add_req.set_Description(params['description'])
    changed = False
    role_add_result=None
    try:
        role_add_result = clt.do_action_with_exception(role_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to add role: %s" % e.message)

    module.exit_json(changed=changed, msg=role_add_result)


def ali_role_update(module,clt):
    #role_name new_role_policy
    required_vars = ['role_name']
    valid_vars = ['new_role_policy']
    params=validate_parameters(required_vars, valid_vars, module)
    role_update_req = UpdateRoleRequest.UpdateRoleRequest()
    role_update_req.set_RoleName(module.params.get('role_name'))
    if 'new_role_policy' in params:
        role_update_req.set_NewAssumeRolePolicyDocument(params['new_role_policy'])
    role_update_req.set_accept_format('json')
    changed = False
    role_update_result=None
    try:
        role_update_result = clt.do_action_with_exception(role_update_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to update role: %s" % e.message)

    module.exit_json(changed=changed, msg=role_update_result)


def ali_role_del(module,clt):
    #role_name
    required_vars = ['role_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    role_del_req = DeleteRoleRequest.DeleteRoleRequest()
    role_del_req.set_RoleName(module.params.get('role_name'))
    role_del_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(role_del_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete role: %s" % e.message)


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'list',  'delete', 'update', 'get'],required=True),
        role_name = dict(required=False),
        role_policy = dict(required=False),
        description = dict(required=False),
        new_role_policy= dict(required=False),
    ))
    invocations = {
        'create': ali_role_add,
        'delete': ali_role_del,
        'list': ali_role_list,
        'update': ali_role_update,
        'get': ali_role_get
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

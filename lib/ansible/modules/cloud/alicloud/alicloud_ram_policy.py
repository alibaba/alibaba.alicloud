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
module: alicloud_ram_policy

short_description: ansible can manage aliyun policy through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage policy.

options:
  state:
    description:
      - Operate policy.
    choices: ['create', 'list', 'get',  'delete', 'create_with_version', 'get_with_version',  'delete_with_version','list_with_version','set_default_with_version',
                     'attach_to_user','detach_from_user','attach_to_group','detach_from_group','attach_to_role','detach_from_role','list_entities_for_policy','list_policy_for_user',
                     'list_policy_for_group','list_policy_for_role' ]

  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters
    
  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]

  role_name:
    description:
      - The role name. A name is created from the specified role.
    aliases: [ 'name' ]
    
  group_name：
    description:
      - The name of group.
      
  policy_name：
    description:
      - The name of group.
      
  policy_type：
    description:
      - The type of group: 'System' or 'Custom'.

  version_id:
    description:
      - The version  of the policy.

  as_default:
    description:
      - Set the version of policy as default.

  policy_document:
    description:
      - The content of policy.
      
  description:
    description:
      - The description of the policy, with a length limit of [0, 256] characters.
        Leaving it blank means null, which is the default value.
      

extends_documentation_fragment:
    - 

author:
    - Your Name (@zhuweif)

'''

EXAMPLES = '''
#
# Policy Management
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
    - name: create policy
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        policy_document:'{{ policy_document }}'
        description:'{{ description }}'
        state: 'create'
      register: result
    - debug: var=result

    - name: list policy
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'list'
      register: result
    - debug: var=result

    - name: get policy
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'get'
      register: result
    - debug: var=result

    - name: delete policy
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        state: 'delete'
      register: result
    - debug: var=result
    
    - name: create policy with version
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        policy_document:'{{ policy_document }}'
        as_default:'True' or 'False'
        state: 'create_with_version'
      register: result
    - debug: var=result
    
    - name: get policy with version
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        version_id:'{{'version_id'}}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'get_with_version'
      register: result
    - debug: var=result
    
    - name: delete policy with version
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        version_id:'{{'version_id'}}'
        state: 'delete_with_version'
      register: result
    - debug: var=result
    
    - name: list policy with version
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'list_with_version'
      register: result
    - debug: var=result
    
    - name: set a policy with version as default
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        version_id:'{{'version_id'}}'
        state: 'set_default_with_version'
      register: result
    - debug: var=result
    
    - name: attach a policy to a user
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        user_name:'{{ user_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'attach_to_user'
      register: result
    - debug: var=result
    
    - name: detach a policy from a user
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        user_name:'{{ user_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'detach_from_user'
      register: result
    - debug: var=result
    
    - name: attach a policy to a group
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        group_name:'{{ group_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'attach_to_group'
      register: result
    - debug: var=result
    
    - name: detach a policy to a group
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        group_name:'{{ group_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'detach_from_group'
      register: result
    - debug: var=result
    
    - name: attach a policy to a role
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        role_name:'{{ role_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'attach_to_group'
      register: result
    - debug: var=result
    
    - name: detach a policy to a role
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        role_name:'{{ role_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'detach_to_group'
      register: result
    - debug: var=result
    
    - name: list all enties for policy
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        policy_name:'{{ policy_name }}'
        policy_type:'{{'System' or 'Custom'}}'
        state: 'list_entities_for_policy'
      register: result
    - debug: var=result
    
    - name: list all policies for user
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'list_policy_for_user'
      register: result
    - debug: var=result
    
    - name: list all policies for group
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'list_policy_for_group'
      register: result
    - debug: var=result
    
     - name: list all policies for role
      alicloud_ram_policy:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'list_policy_for_role'
      register: result
    - debug: var=result
'''

import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import ListPoliciesRequest
from aliyunsdkram.request.v20150501 import CreatePolicyRequest
from aliyunsdkram.request.v20150501 import GetPolicyRequest
from aliyunsdkram.request.v20150501 import CreatePolicyVersionRequest
from aliyunsdkram.request.v20150501 import DeletePolicyRequest
from aliyunsdkram.request.v20150501 import GetPolicyVersionRequest
from aliyunsdkram.request.v20150501 import DeletePolicyVersionRequest
from aliyunsdkram.request.v20150501 import ListPolicyVersionsRequest

from aliyunsdkram.request.v20150501 import SetDefaultPolicyVersionRequest
from aliyunsdkram.request.v20150501 import AttachPolicyToUserRequest
from aliyunsdkram.request.v20150501 import DetachPolicyFromUserRequest
from aliyunsdkram.request.v20150501 import AttachPolicyToGroupRequest
from aliyunsdkram.request.v20150501 import DetachPolicyFromGroupRequest
from aliyunsdkram.request.v20150501 import AttachPolicyToRoleRequest
from aliyunsdkram.request.v20150501 import DetachPolicyFromRoleRequest
from aliyunsdkram.request.v20150501 import ListEntitiesForPolicyRequest
from aliyunsdkram.request.v20150501 import ListPoliciesForUserRequest
from aliyunsdkram.request.v20150501 import ListPoliciesForGroupRequest
from aliyunsdkram.request.v20150501 import ListPoliciesForRoleRequest

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
        'policy_type': 'policy_type',
        'policy_name': 'policy_name',
        'policy_document': 'policy_document',
        'as_default': 'as_default',
        'version_id': 'version_id',
        'user_name': 'user_name',
        'role_name': 'role_name',
        'group_name': 'group_name',
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


def ali_policy_list(module,clt):
    #policy_type: System or Custom
    required_vars = ['']
    valid_vars = ['policy_type']
    params = validate_parameters(required_vars, valid_vars, module)
    policy_list_req=ListPoliciesRequest.ListPoliciesRequest()
    policy_list_req.set_accept_format('json')
    if 'policy_type' in params:
        policy_list_req.set_PolicyType(params['policy_type'])
    try:
        result=clt.do_action_with_exception(policy_list_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policies: " % e.message)


def ali_policy_add(module, clt):
    #policy_name, description, policy_document
    required_vars = ['policy_name', 'policy_document']
    valid_vars = ['description']
    params=validate_parameters(required_vars, valid_vars, module)
    policy_add_req = CreatePolicyRequest.CreatePolicyRequest()
    policy_add_req.set_PolicyDocument(module.params.get('policy_document'))
    policy_add_req.set_PolicyName(module.params.get('policy_name'))
    if 'description' in params:
        policy_add_req.set_Description(params['description'])
        policy_add_req.set_accept_format('json')
    changed = False
    policy_add_result=None
    try:
        policy_add_result = clt.do_action_with_exception(policy_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to create user: %s" % e.message)

    module.exit_json(changed=changed, msg=policy_add_result)


def ali_policy_get(module,clt):
    required_vars = ['policy_name','policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_get_req = GetPolicyRequest.GetPolicyRequest()
    policy_get_req.set_PolicyName(module.params.get('policy_name'))
    policy_get_req.set_PolicyType(module.params.get('policy_type'))
    policy_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(policy_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get policy: %s" % e.message)


def ali_policy_del(module,clt):
    required_vars = ['policy_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_del_req = DeletePolicyRequest.DeletePolicyRequest()
    policy_del_req.set_PolicyName(module.params.get('policy_name'))
    policy_del_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_del_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete policy: %s" % e.message)


def ali_policy_ver_add(module, clt):
    #policy_name, policy_document, as_default
    required_vars = ['policy_name', 'policy_document']
    valid_vars = ['as_default']
    params=validate_parameters(required_vars, valid_vars, module)
    policy_version_add_req = CreatePolicyVersionRequest.CreatePolicyVersionRequest()
    policy_version_add_req.set_PolicyDocument(module.params.get('policy_document'))
    policy_version_add_req.set_PolicyName(module.params.get('policy_name'))
    if 'as_default' in params:
        policy_version_add_req.set_SetAsDefault(params['as_default'])
    policy_version_add_req.set_accept_format('json')
    changed = False
    policy_version_add_result=None
    try:
        policy_version_add_result = clt.do_action_with_exception(policy_version_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to create policy with version: %s" % e.message)

    module.exit_json(changed=changed, msg=policy_version_add_result)


def ali_policy_ver_get(module,clt):
    required_vars = ['policy_name', 'policy_type', 'version_id']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_ver_get_req = GetPolicyVersionRequest.GetPolicyVersionRequest()
    policy_ver_get_req.set_PolicyName(module.params.get('policy_name'))
    policy_ver_get_req.set_PolicyType(module.params.get('policy_type'))
    policy_ver_get_req.set_VersionId(module.params.get('version_id'))
    policy_ver_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(policy_ver_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get policy with version: %s" % e.message)


def ali_policy_ver_del(module,clt):
    required_vars = ['policy_name', 'version_id']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_ver_del_req = DeletePolicyVersionRequest.DeletePolicyVersionRequest()
    policy_ver_del_req.set_PolicyName(module.params.get('policy_name'))
    policy_ver_del_req.set_VersionId(module.params.get('version_id'))
    policy_ver_del_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_ver_del_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete policy with version: %s" % e.message)


def ali_policy_ver_list(module,clt):
    required_vars = ['policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_ver_list_req = ListPolicyVersionsRequest.ListPolicyVersionsRequest()
    policy_ver_list_req.set_PolicyName(module.params.get('policy_name'))
    policy_ver_list_req.set_PolicyType(module.params.get('policy_type'))
    policy_ver_list_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_ver_list_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policy with version: %s" % e.message)


def ali_policy_ver_set_default(module, clt):
    #policy_name, policy_document, as_default
    required_vars = ['policy_name', 'version_id']
    valid_vars = ['']
    params=validate_parameters(required_vars, valid_vars, module)
    policy_version_set_default_req = SetDefaultPolicyVersionRequest.SetDefaultPolicyVersionRequest()
    policy_version_set_default_req.set_VersionId(module.params.get('version_id'))
    policy_version_set_default_req.set_PolicyName(module.params.get('policy_name'))
    policy_version_set_default_req.set_accept_format('json')
    changed = False
    policy_version_set_default_result=None
    try:
        policy_version_set_default_result = clt.do_action_with_exception(policy_version_set_default_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to set policy with version as default: %s" % e.message)

    module.exit_json(changed=changed, msg=policy_version_set_default_result)


def ali_policy_user_attach(module,clt):
    #group_name
    required_vars = ['user_name', 'policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_add_user_req = AttachPolicyToUserRequest.AttachPolicyToUserRequest()
    policy_add_user_req.set_PolicyName(module.params.get('policy_name'))
    policy_add_user_req.set_PolicyType(module.params.get('policy_type'))
    policy_add_user_req.set_UserName(module.params.get('user_name'))
    policy_add_user_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_add_user_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to attach policy to user: %s" % e.message)


def ali_policy_user_detach(module,clt):
    required_vars = ['user_name', 'policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_del_user_req = DetachPolicyFromUserRequest.DetachPolicyFromUserRequest()
    policy_del_user_req.set_PolicyName(module.params.get('policy_name'))
    policy_del_user_req.set_PolicyType(module.params.get('policy_type'))
    policy_del_user_req.set_UserName(module.params.get('user_name'))
    policy_del_user_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_del_user_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to detach  policy  from user: %s" % e.message)


def ali_policy_group_attach(module,clt):
    #group_name
    required_vars = ['group_name', 'policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_add_group_req = AttachPolicyToGroupRequest.AttachPolicyToGroupRequest()
    policy_add_group_req.set_PolicyName(module.params.get('policy_name'))
    policy_add_group_req.set_PolicyType(module.params.get('policy_type'))
    policy_add_group_req.set_GroupName(module.params.get('group_name'))
    policy_add_group_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_add_group_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to attach  policy to group: %s" % e.message)


def ali_policy_group_detach(module,clt):
    required_vars = ['group_name', 'policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_del_group_req = DetachPolicyFromGroupRequest.DetachPolicyFromGroupRequest()
    policy_del_group_req.set_PolicyName(module.params.get('policy_name'))
    policy_del_group_req.set_PolicyType(module.params.get('policy_type'))
    policy_del_group_req.set_GroupName(module.params.get('group_name'))
    policy_del_group_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_del_group_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to detach  policy  from group: %s" % e.message)


def ali_policy_role_attach(module,clt):
    #group_name
    required_vars = ['role_name', 'policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_add_role_req = AttachPolicyToRoleRequest.AttachPolicyToRoleRequest()
    policy_add_role_req.set_PolicyName(module.params.get('policy_name'))
    policy_add_role_req.set_PolicyType(module.params.get('policy_type'))
    policy_add_role_req.set_RoleName(module.params.get('role_name'))
    policy_add_role_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_add_role_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to attach policy to role: %s" % e.message)


def ali_policy_role_detach(module,clt):
    required_vars = ['role_name', 'policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_del_role_req = DetachPolicyFromRoleRequest.DetachPolicyFromRoleRequest()
    policy_del_role_req.set_PolicyName(module.params.get('policy_name'))
    policy_del_role_req.set_PolicyType(module.params.get('policy_type'))
    policy_del_role_req.set_RoleName(module.params.get('role_name'))
    policy_del_role_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_del_role_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to detach  policy from role: %s" % e.message)


def ali_policy_entity_list(module,clt):
    required_vars = ['policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_entity_list_req = ListEntitiesForPolicyRequest.ListEntitiesForPolicyRequest()
    policy_entity_list_req.set_PolicyName(module.params.get('policy_name'))
    policy_entity_list_req.set_PolicyType(module.params.get('policy_type'))
    policy_entity_list_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_entity_list_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policy with entities: %s" % e.message)


def ali_policy_entity_list(module,clt):
    required_vars = ['policy_name', 'policy_type']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    policy_entity_list_req = ListEntitiesForPolicyRequest.ListEntitiesForPolicyRequest()
    policy_entity_list_req.set_PolicyName(module.params.get('policy_name'))
    policy_entity_list_req.set_PolicyType(module.params.get('policy_type'))
    policy_entity_list_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(policy_entity_list_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policy with entities: %s" % e.message)


def ali_user_policy_list(module,clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    user_policy_list_req = ListPoliciesForUserRequest.ListPoliciesForUserRequest()
    user_policy_list_req.set_UserName(module.params.get('user_name'))
    user_policy_list_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(user_policy_list_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policies for user: %s" % e.message)


def ali_group_policy_list(module,clt):
    required_vars = ['group_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    group_policy_list_req = ListPoliciesForGroupRequest.ListPoliciesForGroupRequest()
    group_policy_list_req.set_GroupName(module.params.get('group_name'))
    group_policy_list_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(group_policy_list_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policies for group: %s" % e.message)


def ali_role_policy_list(module,clt):
    required_vars = ['role_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    role_policy_list_req = ListPoliciesForRoleRequest.ListPoliciesForRoleRequest()
    role_policy_list_req.set_RoleName(module.params.get('group_name'))
    role_policy_list_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(role_policy_list_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list policies for role: %s" % e.message)





def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'list', 'get',  'delete', 'create_with_version', 'get_with_version',  'delete_with_version','list_with_version','set_default_with_version',
                     'attach_to_user','detach_from_user','attach_to_group','detach_from_group','attach_to_role','detach_from_role','list_entities_for_policy','list_policy_for_user',
                     'list_policy_for_group','list_policy_for_role' ],required=True),
        user_name= dict(required=False),
        group_name= dict(required=False),
        role_name= dict(required=False),
        policy_name= dict(required=False),
        policy_type= dict(required=False),
        version_id= dict(required=False),
        as_default= dict(required=False),
        policy_document= dict(required=False),
    ))
    invocations = {
        'create': ali_policy_add,
        'delete': ali_policy_del,
        'get': ali_policy_get,
        'list': ali_policy_list,
        'create_with_version': ali_policy_ver_add,
        'get_with_version': ali_policy_ver_get,
        'delete_with_version': ali_policy_ver_del,
        'list_with_version': ali_policy_ver_list,
        'set_default_with_version': ali_policy_ver_set_default,
        'attach_to_user':ali_policy_user_attach,
        'detach_from_user': ali_policy_user_detach,
        'attach_to_group': ali_policy_group_attach,
        'detach_from_group': ali_policy_group_detach,
        'attach_to_role': ali_policy_role_attach,
        'detach_from_role': ali_policy_role_detach,
        'list_entities_for_policy': ali_policy_entity_list,
        'list_policy_for_user': ali_user_policy_list,
        'list_policy_for_group': ali_group_policy_list,
        'list_policy_for_role': ali_role_policy_list,
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

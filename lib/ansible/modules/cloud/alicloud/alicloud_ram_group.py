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
module: alicloud_ram_group

short_description: ansible can manage aliyun group through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage ram-groups. Includes those commands:'create', 'list', 'get', 'delete', 'update', 'add_group_user', 'delete_group_user', 'list_user_groups', 'list_group_users' "

options:
  state:
    description:
      - 'create', 'list', 'get', 'delete', 'update', 'add_group_user', 'delete_group_user', 'list_user_groups', 'list_group_users'
    choices: [ 'create', 'list', 'get', 'delete', 'update', 'add_group_user', 'delete_group_user', 'list_user_groups', 'list_group_users']

  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters

  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]

  group_name：
    description:
      - The name of group.

  comments:
    description:
      - The description of the group, with a length limit of [0, 256] characters.
        Leaving it blank means null, which is the default value.

  new_group_name:
  new_coments:
    description:
      - When update user info,those group's properties can be setted.

extends_documentation_fragment:
    - 

author:
    - Your Name (@zhuweif)

'''

EXAMPLES = '''
#
# Group Management
#
# basic provisioning example to manage group
- name: basic provisioning example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing

  tasks:
    - name: create group
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_name:'{{ group_name }}'
        comments:'{{ comments }}'
        state: 'create'
      register: result
    - debug: var=result

    - name: list group
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'list'
      register: result
    - debug: var=result

    - name: get group by name
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_name:'{{ group_name }}'
        state: 'get'
      register: result
    - debug: var=result

    - name: update group 
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_name:'{{ group_name }}'
        new_group_name:'{{ new_group_name }}'
        new_comments:'{{ new_comments }}'
        state: 'update'
      register: result
    - debug: var=result

    - name: delete group
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_name:'{{group_name }}'
        state: 'delete'
      register: result
    - debug: var=result

    - name: add user to group
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        group_name:'{{ group_name }}'
        state: 'add_group_user'
      register: result
    - debug: var=result

    - name: delete user from group
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        group_name:'{{ group_name }}'
        state: 'delete_group_user'
      register: result
    - debug: var=result
    
    - name: list all groups for user
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'list_user_groups'
      register: result
    - debug: var=result
    
    - name: list all users for group
      alicloud_ram_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_name:'{{ group_name }}'
        state: 'list_group_users'
      register: result
    - debug: var=result
'''
import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import ListGroupsRequest,CreateGroupRequest,GetGroupRequest,UpdateGroupRequest,DeleteGroupRequest,AddUserToGroupRequest,RemoveUserFromGroupRequest,ListGroupsForUserRequest,ListUsersForGroupRequest


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
        'new_comments' : 'new_comments',
        'comments' : 'comments'
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


def ali_group_list(module,clt):
    group_list__req = ListGroupsRequest.ListGroupsRequest()
    group_list__req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(group_list__req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list groups: " % e.message)


def ali_group_add(module, clt):
    #group_name comments
    required_vars = ['group_name']
    valid_vars = ['comments']
    params=validate_parameters(required_vars, valid_vars, module)
    group_add_req = CreateGroupRequest.CreateGroupRequest()
    group_add_req.set_GroupName(module.params.get('group_name'))
    if 'comments' in params:
        group_add_req.set_Comments(params['comments'])
    group_add_req.set_accept_format('json')
    changed = False
    group_add_result=None
    try:
        group_add_result = clt.do_action_with_exception(group_add_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to add group: %s" % e.message)

    module.exit_json(changed=changed, msg=group_add_result)


def ali_group_get(module,clt):
    #group_name
    required_vars = ['group_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    group_get_req = GetGroupRequest.GetGroupRequest()
    group_get_req.set_GroupName(module.params.get('group_name'))
    group_get_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(group_get_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get group: %s" % e.message)


def ali_group_update(module,clt):
    #group_name new_group_name new_comments
    required_vars = ['group_name','new_group_name']
    valid_vars = ['new_comments']
    params=validate_parameters(required_vars, valid_vars, module)

    group_update_req = UpdateGroupRequest.UpdateGroupRequest()
    group_update_req.set_GroupName(module.params.get('group_name'))
    group_update_req.set_NewGroupName(module.params.get('new_group_name'))
    if 'new_comments' in params:
        group_update_req.set_NewComments(params['new_comments'])
    group_update_req.set_accept_format('json')
    changed = False
    group_update_result=None
    try:
        group_update_result = clt.do_action_with_exception(group_update_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to update group: %s" % e.message)

    module.exit_json(changed=changed, msg=group_update_result)


def ali_group_del(module,clt):
    #group_name
    required_vars = ['group_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    group_del_req = DeleteGroupRequest.DeleteGroupRequest()
    group_del_req.set_GroupName(module.params.get('group_name'))
    group_del_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(group_del_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete group: %s" % e.message)


def ali_group_user_add(module,clt):
    #group_name
    required_vars = ['user_name', 'group_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    group_add_user_req = AddUserToGroupRequest.AddUserToGroupRequest()
    group_add_user_req.set_GroupName(module.params.get('group_name'))
    group_add_user_req.set_UserName(module.params.get('user_name'))
    group_add_user_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(group_add_user_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to add user to group: %s" % e.message)


def ali_group_user_del(module,clt):
    #group_name user_name
    required_vars = ['user_name', 'group_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    group_del_user_req = RemoveUserFromGroupRequest.RemoveUserFromGroupRequest()
    group_del_user_req.set_GroupName(module.params.get('group_name'))
    group_del_user_req.set_UserName(module.params.get('user_name'))
    group_del_user_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(group_del_user_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete user to group: %s" % e.message)


def ali_user_group_list(module,clt):
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    user_group_list_req = ListGroupsForUserRequest.ListGroupsForUserRequest()
    user_group_list_req.set_UserName(module.params.get('user_name'))
    user_group_list_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(user_group_list_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list user's groups: %s" % e.message)


def ali_group_user_list(module,clt):
    required_vars = ['group_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    group_user_list_req = ListUsersForGroupRequest.ListUsersForGroupRequest()
    group_user_list_req.set_GroupName(module.params.get('group_name'))
    group_user_list_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(group_user_list_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list group's users: %s" % e.message)


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'list', 'get', 'delete', 'update', 'add_group_user', 'delete_group_user', 'list_user_groups', 'list_group_users'],required=True),
        user_name = dict(required=False),
        comments = dict(required=False),
        group_name=dict(required=False),
        new_group_name = dict(required=False),
        new_comments=dict(required=False),
    ))
    invocations = {
        'create': ali_group_add,
        'list': ali_group_list,
        'get': ali_group_get,
        'delete': ali_group_del,
        'update': ali_group_update,
        'add_group_user': ali_group_user_add,
        'delete_group_user': ali_group_user_del,
        'list_user_groups': ali_user_group_list,
        'list_group_users': ali_group_user_list
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

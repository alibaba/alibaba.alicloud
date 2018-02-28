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
module: alicloud_ram_mfa

short_description: ansible can manage aliyun mfa_devices through this module 

version_added: "1.0"

description:
    - "This module allows the user to manage mfa_devices. Includes those commands:'create', 'delete', 'list', 'bind', 'unbind', 'get'"

options:
  state:
    description:
      - 'create', 'delete', 'list',  'bind', 'unbind', 'get' mfa_device
    choices: [ 'create', 'delete', 'list',  'bind', 'unbind', 'get' ]

  alicloud_secret_key:
  alicloud_access_key:
  alicloud_region:
    description:Those connectting-parameters can be setted with os enviorment-variables or parameters

  user_name:
    description:
      - The user name. A name is created from the specified user.
    aliases: [ 'name' ]

  device_name：
    description:
      - The name of mfa device.

  serial_num:
    description:
      - The only symbol to identity the mfa device.
      
  auth_code1:
    description:
      - The dynamic auth_code1.
      
  auth_code2:
    description:
      - The dynamic auth_code2.
      
    

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
    - name: create mfa_device
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        device_name:'{{ device_name }}'
        state: 'create'
      register: result
    - debug: var=result

    - name: list mfa_devices
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: 'list'
      register: result
    - debug: var=result

    - name: bind mfa device to user
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        serial_num:'{{ serial_num }}'
        auth_code1:'{{ auth_code1 }}'
        auth_code2:'{{ auth_code2 }}'
        state: 'bind'
      register: result
    - debug: var=result

    - name: unbind mfa device from user
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        serial_num:'{{ serial_num }}'
        state: 'unbind'
      register: result
    - debug: var=result
    
    - name: get mfa devices for user
      alicloud_ram_mfa:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        user_name:'{{ user_name }}'
        state: 'get'
      register: result
    - debug: var=result
'''


import os
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ansible.module_utils.basic import AnsibleModule
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import CreateVirtualMFADeviceRequest,ListVirtualMFADevicesRequest,DeleteVirtualMFADeviceRequest,BindMFADeviceRequest,UnbindMFADeviceRequest,GetUserMFAInfoRequest


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


def ali_mfa_device_list(module,clt):
    list_mfa_devices_req = ListVirtualMFADevicesRequest.ListVirtualMFADevicesRequest()
    list_mfa_devices_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(list_mfa_devices_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to list mfa_devices: " % e.message)


def ali_mfa_device_add(module, clt):
    #device_name
    required_vars = ['device_name']
    valid_vars = ['']
    params=validate_parameters(required_vars, valid_vars, module)
    add_mfa_dev_req = CreateVirtualMFADeviceRequest.CreateVirtualMFADeviceRequest()
    add_mfa_dev_req.set_accept_format('json')
    add_mfa_dev_req.set_VirtualMFADeviceName(module.params.get('device_name'))

    changed = False
    mfa_device_add_result=None
    try:
        mfa_device_add_result = clt.do_action_with_exception(add_mfa_dev_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to add mfa_device: %s" % e.message)

    module.exit_json(changed=changed, msg=mfa_device_add_result)


def ali_mfa_device_del(module,clt):
    #serial_num
    required_vars = ['serial_num']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    del_mfa_device_req = DeleteVirtualMFADeviceRequest.DeleteVirtualMFADeviceRequest()
    del_mfa_device_req.set_SerialNumber(module.params.get('serial_num'))
    del_mfa_device_req.set_accept_format('json')
    try:
         result=clt.do_action_with_exception(del_mfa_device_req)
         module.exit_json(changed=True, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to delete mfa_device: %s" % e.message)


def ali_mfa_device_bind(module,clt):
    #user_name, serial_num, auth_code1, auth_code2
    required_vars = ['user_name','serial_num','auth_code1', 'auth_code2']
    valid_vars = ['']
    params = validate_parameters(required_vars, valid_vars, module)

    bind_mfa_device_req = BindMFADeviceRequest.BindMFADeviceRequest()
    bind_mfa_device_req.set_SerialNumber(module.params.get('serial_num'))
    bind_mfa_device_req.set_UserName(module.params.get('user_name'))
    bind_mfa_device_req.set_AuthenticationCode1(module.params.get('auth_code1'))
    bind_mfa_device_req.set_AuthenticationCode2(module.params.get('auth_code2'))
    bind_mfa_device_req.set_accept_format('json')
    changed = False
    bind_mfa_device_result=None
    try:
        bind_mfa_device_result = clt.do_action_with_exception(bind_mfa_device_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to bind mfa_device: %s" % e.message)

    module.exit_json(changed=changed, msg=bind_mfa_device_result)


def ali_mfa_device_unbind(module,clt):
    #user_name, serial_num
    required_vars = ['user_name','serial_num']
    valid_vars = ['']
    params = validate_parameters(required_vars, valid_vars, module)

    unbind_mfa_device_req = UnbindMFADeviceRequest.UnbindMFADeviceRequest()
    unbind_mfa_device_req.set_SerialNumber(module.params.get('serial_num'))
    unbind_mfa_device_req.set_UserName(module.params.get('user_name'))
    unbind_mfa_device_req.set_accept_format('json')
    changed = False
    unbind_mfa_device_result=None
    try:
        unbind_mfa_device_result = clt.do_action_with_exception(unbind_mfa_device_req)
        changed = True
    except ServerException as e:
        module.fail_json(msg="Failed to unbind mfa_device: %s" % e.message)

    module.exit_json(changed=changed, msg=unbind_mfa_device_result)


def ali_mfa_user_get(module,clt):
    #user_name
    required_vars = ['user_name']
    valid_vars = ['']
    validate_parameters(required_vars, valid_vars, module)
    get_user_mfa_info_req = GetUserMFAInfoRequest.GetUserMFAInfoRequest()
    get_user_mfa_info_req.set_UserName(module.params.get('user_name'))
    get_user_mfa_info_req.set_accept_format('json')
    try:
        result = clt.do_action_with_exception(get_user_mfa_info_req)
        module.exit_json(changed=False, msg=result)
    except ServerException as e:
        module.fail_json(msg="Failed to get mfa devices by user: %s" % e.message)


def main():
    argument_spec = ali_connection_spec()
    argument_spec.update(dict(
        state=dict(
            choices=['create', 'delete', 'list',  'bind', 'unbind', 'get'],required=True),
        user_name = dict(required=False),
        serial_num=dict(required=False),
        auth_code1=dict(required=False),
        auth_code2=dict(required=False),
        device_name=dict(required=False),
    ))
    invocations = {
        'create': ali_mfa_device_add,
        'delete': ali_mfa_device_del,
        'list': ali_mfa_device_list,
        'bind': ali_mfa_device_bind,
        'unbind': ali_mfa_device_unbind,
        'get': ali_mfa_user_get
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

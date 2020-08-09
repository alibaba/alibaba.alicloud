#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_key_pair
short_description: Create, Import, Delete ECS KeyPairs in Alibaba Cloud.
description:
    - Create, Import, Delete ECS KeyPairs in Alibaba Cloud.
options:
  state:
    description:
      - If I(state=present), key pair will be created.
      - If I(state=absent), key pair will be removed.
    choices: ['present', 'absent']
    default: 'present'
    type: str
  name:
    description:
      - The name of key pair, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, "_" or "-".
        It cannot begin with http:// or https://.
    required: True
    aliases: ['key_pair_name']
    type: str
  public_key:
    description:
      - The public key of the key pair. import key pair to Alicloud.
    type: str
  force:
    description:
      - Force overwrite of already existing key pair if key has changed.
    default: True
    type: bool
  tags:
    description:
      - A hash/dictionaries of key pair tags. C({"key":"value"})
    type: dict
requirements:
    - "python >= 3.6"
    - "footmark >= 1.21.0"
extends_documentation_fragment:
    - alicloud
author:
  - "Yang Liu (@liuyangc3)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Create a new key pair
  ali_key_pair:
    name: my_keypair

- name: Import a key pair using provided public_key
  ali_key_pair:
    name: my_keypair
    public_key: 'ssh-rsa AAAAxyz...== me@example.com'
    
- name: Create key pair using public_key obtained using 'file' lookup plugin
  ali_key_pair:
    name: my_keypair
    public_key: "{{ lookup('file', '/path/to/public_key/id_rsa.pub') }}"

# try creating a key pair with the name of an already existing keypair
# but don't overwrite it even if the key is different (force=false)
- name: try creating a key pair with name of an already existing keypair
  ali_key_pair:
    name: my_existing_keypair
    public_key: 'ssh-rsa AAAAxyz...== me@example.com'
    force: false

- name: Delete the existing key pair
  ali_key_pair:
    name: my_keypair
    state: absent
"""

RETURN = '''
key:
    description: Dictionary of key pair, (this is set to null when state is absent)
    returned: always
    type: complex
    contains:
        name:
            description: The name of the key pair
            returned: always
            type: str
            sample: "mykey"
        fingerprint:
            description: fingerprint of the key
            returned: when state is present
            type: str
            sample: 'b0:22:49:61:d9:44:9d:0c:7e:ac:8a:32:93:21:6c:e8:fb:59:62:43'
        private_key:
            description: private key of a newly created key pair 
            returned: when state is present (public_key is not provided)
            type: str
            sample: "-----BEGIN RSA PRIVATE KEY-----\nMII..."
        tags:
            description: tags attached to the key pair
            returned: always
            type: dict
            sample: {"Name": "My key", "env": "staging"}
        creation_time:
            description: The time the key pair was created.
            returned: always
            type: str
            sample: '2018-06-24T15:14:45Z'
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def key_pair_exists(conn, module, key_pair_name):
    try:
        for kp in conn.describe_key_pairs():
            if key_pair_name and kp.name != key_pair_name:
                continue
            return kp
    except Exception as e:
        module.fail_json(msg="Couldn't get matching key pair: {0}".format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True),
        public_key=dict(type='str'),
        force=dict(type='bool', default=True),
        tags=dict(type='dict')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_key_pair.')

    ecs = ecs_connect(module)

    # Get values of variable
    state = module.params['state']
    key_pair_name = module.params['name']
    force = module.params['force']
    public_key = module.params.get('public_key', '')

    changed = False
    key_pair = key_pair_exists(ecs, module, key_pair_name)

    if state == 'absent':
        if not key_pair:
            module.exit_json(changed=changed, key={})
        try:
            changed = key_pair.delete()
            module.exit_json(changed=changed, key={})
        except ECSResponseError as ex:
            module.fail_json(msg='Unable to delete key_pair: {0}, error: {1}'.format(key_pair.name, ex))

    if str(key_pair_name).startswith('http://') or str(key_pair_name).startswith('https://'):
        module.fail_json(msg='key pair name can not start with http:// or https://')

    if key_pair and force:
        try:
            key_pair.delete()
        except ECSResponseError as ex:
            module.fail_json(msg='Unable to force delete key_pair: {0}, error: {1}'.format(key_pair.name, ex))

    if not key_pair:
        try:
            params = module.params
            params['client_token'] = "Ansible-Alicloud-{0}-{1}".format(hash(str(module.params)), str(time.time()))
            params['key_pair_name'] = key_pair_name
            if public_key:
                key_pair = ecs.import_key_pair(**params)
            else:
                key_pair = ecs.create_key_pair(**params)
            module.exit_json(changed=True, key=key_pair)
        except ECSResponseError as e:
            module.fail_json(msg='Unable to create key pair, error: {0}'.format(e))


if __name__ == '__main__':
    main()

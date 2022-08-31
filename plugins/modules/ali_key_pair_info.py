#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
#  This file is part of Ansible
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
module: ali_key_pair_info
short_description: Gather facts on ECS key pair of Alibaba Cloud OSS.
description:
     - Gather facts on ECS key pair of Alibaba Cloud OSS. 
       This module fetches data from the Open API in Alicloud.

options:
    key_pair_name:
        description:
          - The name of the key pair. The asterisk (*) symbol can be used as a wild card 
            in regular expressions to query key pairs by fuzzy match. Sample patterns.
        aliases: [ 'name' ]  
    key_pair_finger_print:
        description:
          - The fingerprint of the key pair. The fingerprint uses the message-digest algorithm
            5 (MD5) based on the public key fingerprint format defined in RFC 4716.       
author:
    - "Yang Liu (@liuyangc3)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Get the existing key pair
  alibaba.alicloud.ali_key_pair_info:
    key_pair_name: mysshkey

- name: Get the existing groups
  alibaba.alicloud.ali_key_pair_info:
    key_pair_finger_print: ''

'''

RETURN = '''
key_pairs:
    description: The list all key pairs that match of name or asterisk (*) name.
    returned: always
    type: complex
    contains:
        key_pair_name:
            description: The key pair name.
            returned: always
            type: str
            sample: mysshkey
        create_date:
            description: The date and time when the key pair was created.
            returned: always
            type: str
            sample: '2015-01-23T12:33:18Z'
        resource_group_id:
            description: The Resource Group Id.
            returned: always
            type: str
            sample: ""
        name:
            description: alias of 'key_pair_name'.
            returned: always
            type: str
            sample: mysshkey
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError, OSSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        key_pair_name=dict(type='str'), aliases=["name"]),
        key_pair_finger_print=dict(type="str")
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    filters = {}
    key_pair_name = module.params['key_pair_name']
    if key_pair_name:
        filters['key_pair_name'] = key_pair_name

    key_pair_finger_print = module.params['key_pair_finger_print']
    if key_pair_finger_print:
        filters['key_pair_finger_print'] = key_pair_finger_print

    changed = False
    key_pairs = []
    try:
        for key_pair in ecs_connect(module).describe_key_pairs(**filters):
            key_pairs.append(key_pair.get().read())

    except ECSResponseError as e:
        module.fail_json(msg='Error in describe_key_pairs: {0}'.format(e))

    module.exit_json(changed=changed, key_pairs=key_pairs)


if __name__ == '__main__':
    main()

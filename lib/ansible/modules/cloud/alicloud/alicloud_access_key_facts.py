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


from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_access_key_facts
version_added: "2.5"
short_description: Gather facts on access_keys of Alibaba Cloud Ram User.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called by a user name.

options:
    user_name:
      description:
        - A name of a ram user.
author:
    - Zhu Wei (@zhuweif)
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch disk details according to setting different filters
- name: Fetch access_key details example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    user_name:
      - zhuweif@chanjet.com
  tasks:
    - name: Find all access_keys of a ram user
      alicloud_access_key_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
      register: access_keys_by_user
    - debug: var=access_keys_by_user

'''

RETURN = '''
access_keys:
    description: Details about the access_key.
    returned: when success
    type: list
    sample: [
        {
          "access_key_id": "0wNEpMMlzy7szvai",
          "status": "Active",
          "create_date": "2015-01-23T12:33:18Z"
        },
        {
          "access_key_id": "WnIWUruvfaDT37vQ",
          "status": "Inactive",
          "create_date": "2015-03-24T21:12:21Z"
        }
    ]
total:
    description: The number of all access_keys of the ram user.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec,ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(accesskey):
    """
        Retrieves  information from an access_key
        ID and returns it as a dictionary
    """
    return {
        'access_key_id': accesskey.access_key_id,
        'access_key_secret': accesskey.access_key_secret,
        'status': accesskey.status,
        'create_date': accesskey.create_date
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        user_name=dict(required=True),
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)
    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    user_name = module.params['user_name']
    result = []
    ids = []
    try:
        ram = ram_connect(module)
        for accesskey in ram.list_access_keys(user_name=user_name):
            result.append(get_info(accesskey))
            module.exit_json(changed=False, access_keys=result, total=len(result))
    except ECSResponseError as e:
        module.fail_json(msg='Error in describe access_keys: %s' % str(e))


if __name__ == '__main__':
    main()
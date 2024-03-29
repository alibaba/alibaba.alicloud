#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. <xiaozhu36>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_ram_access_key_info
short_description: List the AccessKeys of a RAM user in Alibaba Cloud.
description:
     - List the AccessKeys of a RAM user.
options:
  user_name:
    description:
      - The username of the RAM user. If this parameter is not set when the user logs on to the console, 
        the AccessKeys of this user are displayed.
    type: str
    aliases: ['name']
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.17.0"
extends_documentation_fragment:
    - alibaba.alicloud.alicloud
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.

- name: Get infos about all Users
  alibaba.alicloud.ali_ram_user_info:

- name: Get infos about a particular User using name_prefix
  alibaba.alicloud.ali_ram_user_info:
    name_prefix: "ansible"
'''

RETURN = '''
users:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        access_key_id:
            description: The AccessKeyId.
            returned: always
            type: str
            sample: 0wNEpMMlzy7s****
        create_date:
            description: The date and time when the AccessKey was created.
            returned: always
            type: str
            sample: '2015-01-23T12:33:18Z'
        status:
            description: The status of the AccessKey.
            returned: always
            type: str
            sample: Active
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.alibaba.alicloud.plugins.module_utils.alicloud_ecs import ecs_argument_spec, ram_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RAMResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        user_name=dict(type='str', aliases=['name'])
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")
    try:
        access_key = []
        for access in ram_connect(module).list_access_keys(**module.params):
            access_key.append(access.read())
        module.exit_json(changed=False, access_keys=access_key)
    except Exception as e:
        module.fail_json(msg=str("Unable to list access_keys, error:{0}".format(e)))


if __name__ == '__main__':
    main()

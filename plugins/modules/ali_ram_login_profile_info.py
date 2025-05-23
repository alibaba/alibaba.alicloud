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
module: ali_ram_login_profile_info
short_description: Gather info on ram login profile in Alibaba Cloud.
description:
     - Gather info on ram login profile in Alibaba Cloud.
options:
  user_name:
    description:
      - The username.
    type: str
    required: True
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
- name: Get the existing login profile.
  alibaba.alicloud.ali_ram_login_profile_info:
    user_name: ansible

'''

RETURN = '''
users:
    description: Returns an array of complex objects as described below.
    returned: always
    type: complex
    contains:
        create_date:
            description: The creation time.
            returned: always
            type: str
            sample: '2015-01-23T12:33:18Z'
        mfabind_required:
            description: Indicates that you must attach an MFA device.
            returned: always
            type: bool
            sample: False
        password_reset_required:
            description: Indicates that you must change your password upon next logon.
            returned: always
            type: bool
            sample: False
        user_name:
            description: The username.
            returned: always
            type: str
            sample: Alice
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
        user_name=dict(type='str', required=True, aliases=['name'])
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    user_name = module.params['user_name']
    try:
        profile = ram_connect(module).get_login_profile(user_name=user_name)
        if not profile:
            module.exit_json(changed=False, profile=None)
        module.exit_json(changed=False, profile=profile.read())
    except Exception as e:
        module.fail_json(msg=str("Unable to get profile, error:{0}".format(e)))


if __name__ == '__main__':
    main()

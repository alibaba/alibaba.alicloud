#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017-present Ansible Project
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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_rds_account_info
version_added: "2.9"
short_description: Gather info on RDS accounts of Alibaba Cloud.
description:
     - Gather info on RDS accounts of Alibaba Cloud and Support to use name_prefix to filter accounts.
options:
    db_instance_id:
      description:
        - The ID of the instance.
      aliases: ['instance_id']
      required: True
      type: str
    name_prefix:
      description:
        - Use name prefix to filter accounts.
      type: str
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.16.0"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
# Fetch rds account details according to setting different filters
- name: No Changed. get rds account with name_prefix.
  ali_rds_account_info:
    db_instance_id: '{{ db_instance_id }}'
    name_prefix: account_

- name: No Changed. Retrieving all rds account
  ali_rds_account_info:
    db_instance_id: '{{ db_instance_id }}'
"""

RETURN = '''
rds_accounts:
    description: Details about the rds accounts.
    returned: when success
    type: complex
    contains:
        account_description:
            description: Account remarks
            returned: always
            type: string
            sample: account from ansible
        account_name:
            description: The name of account.
            returned: always
            type: string
            sample: account
        account_type:
            description: Privilege type of account.
            returned: always
            type: string
            sample: Normal
        db_instance_id:
            description: The ID of the instance to which the account belongs.
            returned: always
            type: string
            sample: rm-2zeib35bbexxxxxx
        name:
            description: alias of account_name.
            returned: always
            type: string
            sample: account
        account_status:
            description: The status of the account.
            returned: always
            type: string
            sample: Available
        account_type:
            description: The type of the account.
            returned: always
            type: string
            sample: Super
        status:
            description: alias of account_status.
            returned: always
            type: string
            sample: Available
        type:
            description: alias of account_type.
            returned: always
            type: string
            sample: Super
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, rds_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RDSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        db_instance_id=dict(type='str', aliases=['instance_id'], required=True),
        name_prefix=dict(type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json("Package 'footmark' required for this module.")

    # Get values of variable
    db_instance_id = module.params['db_instance_id']
    name_prefix = module.params['name_prefix']
    result = []
    try:
        rds = rds_connect(module)
        for account in rds.describe_accounts(db_instance_id=db_instance_id):
            if name_prefix and not account.name.startswith(name_prefix):
                continue
            result.append(account.read())
        module.exit_json(changed=False, rds_accounts=result)
    except Exception as e:
        module.fail_json(msg="Unable to describe rds accounts, and got an error: {0}.".format(e))


if __name__ == "__main__":
    main()

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
module: ali_rds_account
version_added: "2.9"
short_description: Create, Delete, Modyfy, Reset rds account, Grant or Revoke privilege in Alibaba Cloud.
description:
  - This module allows the user to manage rds account. Includes support for creating, deleting,
    reseting and modifying rds account, granting or revoking privilege.
  - An unique ali_rds_account module is co-determined by parameters db_instance_id and account_name. 
options:
  state:
    description:
      - If I(state=present), account will be created.
      - If I(state=present) and account_password, account exists, it will reset account password.
      - If I(state=present) and account_description exists, it will modify description.
      - If I(state=present) and db_name, account_privilege exists, it will grant account privilege.
      - If I(state=absent), and db_name exists, it will revoke account privilege.
      - If I(state=absent), account will be removed.      
    default: present
    choices: ['present', 'absent']
    type: str
  db_instance_id:
    description:
      - The ID of the instance.
      - This is used in combination with C(account_name) to determine if the account already exists.
    aliases: ['instance_id']
    required: true
    type: str
  account_name:
    description:
      - It may consist of lower case letters, numbers and underlines, and must start with a letter and have no more than 16 characters.
      - This is used in combination with C(db_instance_id) to determine if the account already exists.
    required: true
    aliases: ['name']
    type: str
  account_password:
    description:
      - The password of the database account. It contains 8 to 32 characters. at least three of the following four character.
        types (uppercase letters, lowercase letters, digits, and special characters).
        The allowed special characters are ( ! @ # $ & % ^ * ( ) _ + - = )
    aliases: ['password']
    type: str
  account_description:
    description:
      - Account remarks, which cannot exceed 256 characters. It cannot begin with http:// , https:// .
        It must start with a Chinese character or English letter. It can include Chinese and
        English characters/letters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters,
    aliases: ['description']
    type: str
  account_type:
    description:
      - Privilege type of account. Normal for Common privilege; Super for High privilege; Default value is Normal.
    default: Normal
    aliases: ['type']
    choices: ['Normal', 'Super']
    type: str
  db_names:
    description:
      - The names of the database that the account needs to access.
    type: list
  account_privilege:
    description:
      - The account privilege. For MySQL and MariaDB, the values are ReadWrite, ReadOnly, DDLOnly, and DMLOnly.
        For SＱL Server, the values are ReadWrite, ReadOnly, and DBOwner. For PostgreSQL, the value is DBOwner.
    aliases: ['privilege']
    choices: ['ReadOnly', 'ReadWrite', 'DDLOnly', 'DMLOnly', 'DBOwner']
    type: str
author:
    - "He Guimin (@xiaozhu36)"
    - "Li Xue (@lixue323)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.16.0"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
# basic provisioning example to create account
- name: Changed. Create rds account.
  ali_rds_account:
    db_instance_id: '{{ db_instance_id }}'
    account_name: account
    account_password: Ansible12345
    account_description: account from ansible
    account_type: Normal

- name: Changed. Modify rds account password.
  ali_rds_account:
    db_instance_id: '{{ db_instance_id }}'
    account_name: account
    account_password: Ansible12345_new

- name: Changed. Modify rds account description.
  ali_rds_account:
    db_instance_id: '{{ db_instance_id }}'
    account_name: account
    account_description: account from ansible

- name: Changed. Grant rds account privilege
  ali_rds_account:
    db_instance_id: '{{ db_instance_id }}'
    account_name: account
    db_names: ['{{ db_name }}', '{{ db_name1 }}']
    account_privilege: ReadWrite

- name: Changed. revoke account privilege
  ali_rds_account:
    db_instance_id: '{{ db_instance_id }}'
    account_name: account
    db_names: ['{{ db_name }}', '{{ db_name1 }}']
    state: absent

- name: Changed. Deleting account
  ali_rds_account:
    state: absent
    db_instance_id: '{{ db_instance_id }}'
    account_name: account
"""

RETURN = '''
account:
    description: account info.
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
            description: alias of status.
            returned: always
            type: string
            sample: Available
        type:
            description: alias of type.
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
        state=dict(default='present', choices=['present', 'absent']),
        db_names=dict(type='list'),
        db_instance_id=dict(type='str', aliases=['instance_id'], required=True),
        account_name=dict(type='str', aliases=['name'], required=True),
        account_password=dict(type='str', aliases=['password']),
        account_privilege=dict(aliases=['privilege'], choices=['ReadOnly', 'ReadWrite', 'DDLOnly', 'DMLOnly', 'DBOwner']),
        account_description=dict(type='str', aliases=['description']),
        account_type=dict(default='Normal', type='str', choices=['Normal', 'Super'], aliases=['type'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    rds = rds_connect(module)

    if HAS_FOOTMARK is False:
        module.fail_json("Footmark required for this module")

    # Get values of variable
    state = module.params['state']
    db_instance_id = module.params['db_instance_id']
    account_name = module.params['account_name']
    account_password = module.params['account_password']
    account_privilege = module.params['account_privilege']
    account_description = module.params['account_description']
    db_names = module.params['db_names']

    current_account = None
    changed = False

    try:
        current_account_list = rds.describe_accounts(db_instance_id=db_instance_id, account_name=account_name)
        if len(current_account_list) == 1:
            current_account = current_account_list[0]
    except Exception as e:
        module.fail_json(msg=str("Unable to describe accounts, error:{0}".format(e)))

    if state == "absent":
        if current_account:
            if db_names:
                try:
                    changed = current_account.revoke_privilege(db_names)
                    module.exit_json(changed=True, account=current_account.get().read())
                except Exception as e:
                    module.fail_json(msg=str("Unable to revoke privilege error:{0}".format(e)))
            try:
                changed = current_account.delete()
                module.exit_json(changed=True, account={})
            except Exception as e:
                module.fail_json(msg=str("Unable to delete account error:{0}".format(e)))
        module.fail_json(msg="There is no account to revoke database privilege or delete. Please specify an account using 'account_name', and try again.")

    if account_password and current_account:
        try:
            changed = current_account.reset(account_password)
        except Exception as e:
            module.fail_json(msg=str("Unable to reset account password error:{0}".format(e)))

    if not current_account:
        try:
            current_account = rds.create_account(**module.params)
            changed = True
        except Exception as e:
            module.fail_json(msg=str("Unable to create account error:{0}".format(e)))

    if account_description and account_description != current_account.description:
        try:
            changed = current_account.modify_description(description=account_description)
        except Exception as e:
            module.fail_json(msg=str("Unable to modify account description error:{0}".format(e)))

    if db_names and account_privilege:
        try:
            changed = current_account.grant_privilege(db_names, account_privilege)
        except Exception as e:
            module.fail_json(msg=str("Unable to grant privilege error:{0}".format(e)))
    module.exit_json(changed=changed, account=current_account.read())


if __name__ == "__main__":
    main()

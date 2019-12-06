#!/usr/bin/python
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: alicloud_rds_account
version_added: "1.0.9"
short_description: Create, Delete, Modyfy, Reset rds account, Grant or Revoke privilege.
description:
  - This module allows the user to manage rds account. Includes support for creating, deleting,
    reseting and modifying rds account, granting or revoking privilege.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix "ali" will be more concise.
  alternative: Use M(ali_rds_account) instead.
options:
  state:
    description:
      - The state of the account after operating.
    default: present
    choices: [ 'present', 'absent']
  db_instance_id:
    description:
      - Id of rds instance.
    required: true
  account_name:
    description:
      - Operation account requiring a uniqueness check.
        It may consist of lower case letters, numbers and underlines, and must start with a letter and have no more than 16 characters.
    required: true
    aliases: ['name']
  account_password:
    description:
      - Operation password. It may consist of letters, digits, or underlines, with a length of 6 to 32 characters, Required when C(account_password != "")
    aliases: ['password']
  description:
    description:
      - Account remarks, which cannot exceed 256 characters. It cannot begin with http:// , https:// .
        It must start with a Chinese character or English letter. It can include Chinese and
        English characters/letters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters,
  account_type:
    description:
      - Privilege type of account. Normal for Common privilege; Super for High privilege; Default value is Normal.
        This parameter is valid for MySQL 5.5/5.6 only
    default: Normal
    aliases: ['type']
    choices: [ 'Normal', 'Super']
  db_name:
    description:
      - Name of the database associated with this account, Required when C(db_name != "").
  account_privilege:
    description:
      - Account permission.Required when C(account_privilege != "")
    aliases: ['privilege']
    choices: ['ReadOnly', 'ReadWrite']
author:
  - "Li Qiang"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
# basic provisioning example to create account
- name: create account
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    db_instance_id: <your-rds-instance-id>
    account_name: test
    account_password: rohit@123
    description: normal account
    account_type: normal
  tasks:
    - name: create account
      ali_rds_account:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        db_instance_id: '{{ db_instance_id }}'
        account_name: '{{ account_name }}'
        account_password: '{{ account_password }}'
        description: '{{ description }}'
        account_type: '{{ account_type }}'
      register: result
    - debug: var=result

# basic provisioning example to modify account description
- name: modify description
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    db_instance_id: <your-rds-instance-id>
    account_name: test
    description: normal account
  tasks:
    - name: modify description
      ali_rds_account:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        db_instance_id: '{{ db_instance_id }}'
        account_name: '{{ account_name }}'
        description: '{{ description }}'
      register: result
    - debug: var=result

# basic provisioning example to reset an account password
- name: Reset an account password
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    db_instance_id: <your-rds-instance-id>
    account_name: test
    account_password: rohit@123
  tasks:
    - name: reset an account password
      ali_rds_account:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        db_instance_id: '{{ db_instance_id }}'
        account_name: '{{ account_name }}'
        account_password: '{{ account_password }}'
      register: result
    - debug: var=result

# basic provisioning example to delete an account
- name: Delete account
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-hongkong
    state: absent
    db_instance_id: <your-rds-instance-id>
    account_name: test
  tasks:
    - name: delete account
      rds_account:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        db_instance_id: '{{ db_instance_id }}'
        account_name: '{{ account_name }}'
      register: result
    - debug: var=result

# basic provisioning example to grant account permission
- name: grant account permission
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-hongkong
    db_instance_id: <your-rds-instance-id>
    db_name: test
    account_name: account-test
    account_privilege: ReadOnly
  tasks:
    - name: grant account permission
      rds_account:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        db_instance_id: '{{ db_instance_id }}'
        db_name: '{{ db_name }}'
        account_name: '{{ account_name }}'
        account_privilege: '{{ account_privilege }}'
      register: result
    - debug: var=result

# basic provisioning example to revoke account permission
- name: revoke account permission
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-hongkong
    db_instance_id: <your-rds-instance-id>
    db_name: db-test
    account_name: account-test
  tasks:
    - name: revoke account permission
      rds_account:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        db_instance_id: '{{ db_instance_id }}'
        db_name: '{{ db_name }}'
        account_name: '{{ account_name }}'
      register: result
    - debug: var=result
"""

RETURN = '''
account:
    description: account info.
    returned: when success
    type: dict
    sample: {
        "account_description": "",
        "account_name": "testdemoaccount",
        "account_status": "Available",
        "account_type": "Normal",
        "database_privileges": {
            "database_privilege": [
                {
                    "account_privilege": "ReadOnly",
                    "dbname": "testtest"
                }
            ]
         },
         "db_instance_id": "rm-2zey7ir50261bmg42"
    }
account_name:
    description: name of account.
    returned: when success
    type: str
    sample: "testname"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, rds_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RDSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(obj):
    """
    get info from account obj
    :type obj: account object
    :param obj: the object of account
    :return: dict of account info
    """
    if obj:
        return dict(db_instance_id=obj.dbinstance_id,
                    account_name=obj.account_name,
                    account_status=obj.account_status,
                    account_type=obj.account_type,
                    account_description=obj.account_description,
                    database_privileges=obj.database_privileges)
    return {}


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        db_name=dict(type='str'),
        db_instance_id=dict(type='str', required=True),
        account_name=dict(type='str', aliases=['name'], required=True),
        account_password=dict(type='str', aliases=['password']),
        account_privilege=dict(aliases=['privilege'], choices=['ReadOnly', 'ReadWrite']),
        description=dict(type='str'),
        account_type=dict(default='Normal', type='str', choices=['Normal', 'Super']),
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
    description = module.params['description']
    account_type = module.params['account_type']
    db_name = module.params['db_name']

    account_list = []
    current_account = None
    changed = False

    try:
        current_account_list = rds.list_account(db_instance_id, account_name)
        if len(current_account_list) == 1:
            current_account = current_account_list[0]
    except Exception as e:
        module.fail_json(msg=str("Unable to describe accounts, error:{0}".format(e)))

    if state == "absent":
        if current_account:
            if db_name:
                try:
                    changed = current_account.revoke_privilege(db_instance_id, db_name)
                    current_account = rds.list_account(db_instance_id, account_name)[0]
                    module.exit_json(changed=True, account_name=account_name, account=get_info(current_account))
                except Exception as e:
                    module.fail_json(msg=str("Unable to revoke privilege error:{0}".format(e)))
            try:
                changed = current_account.delete(db_instance_id)
                module.exit_json(changed=True, account_name=account_name, account=get_info(current_account))
            except Exception as e:
                module.fail_json(msg=str("Unable to delete account error:{0}".format(e)))
        module.fail_json(msg="There is no account to revoke database privilege or delete. Please specify an account using 'account_name', and try again.")
    if account_password and current_account:
        try:
            changed = current_account.reset(db_instance_id, account_password)
        except Exception as e:
            module.fail_json(msg=str("Unable to reset account password error:{0}".format(e)))
    if not current_account:
        try:
            current_account = rds.create_account(db_instance_id, account_name, account_password, description, account_type)
        except Exception as e:
            module.fail_json(msg=str("Unable to create account error:{0}".format(e)))
    if description and description != current_account.account_description:
        try:
            changed = current_account.modify_description(db_instance_id, description)
            current_account.account_description = description
        except Exception as e:
            module.fail_json(msg=str("Unable to modify account description error:{0}".format(e)))
    if db_name:
        if account_privilege:
            try:
                changed = current_account.grant_privilege(db_instance_id, db_name, account_privilege)
                current_account = current_account_list[0]
            except Exception as e:
                module.fail_json(msg=str("Unable to grant privilege error:{0}".format(e)))
        else:
            module.fail_json(msg="grant privilege failed. Please check your account_privilege and try again.")
    module.exit_json(changed=changed, account_name=account_name, account=get_info(current_account))


if __name__ == "__main__":
    main()

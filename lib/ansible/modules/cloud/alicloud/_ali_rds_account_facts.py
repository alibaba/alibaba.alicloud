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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_rds_account_facts
version_added: "1.5.0"
short_description: Gather facts on RDS accounts of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the RDS account itself.
options:
    db_instance_id:
      description:
        - ID of RDS instance.
    account_names:
      description:
        - A list of RDS account names.
      aliases: ["names"]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
# Fetch rds account details according to setting different filters
- name: fetch rds account details example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    db_instance_id: rm-dj13c34832w21g47j
    account_names:
      - demoaccount
      - testaccount
  tasks:
    - name: Find all accounts in the rds instance
      ali_rds_account_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        db_instance_id: '{{ db_instance_id }}'
      register: all_accounts
    - debug: var=all_accounts
    
    - name: Find accounts in the rds instance by account name
      ali_rds_account_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        db_instance_id: '{{ db_instance_id }}'
        account_names: '{{ account_names }}'
      register: accounts_by_name
    - debug: var=accounts_by_name
"""

RETURN = '''
account_names:
    description: List all account's name of rds instance.
    returned: when success
    type: list
    sample: [ "demoaccount", "testaccount" ]
rds_accounts:
    description: Details about the rds accounts that were created.
    returned: when success
    type: list
    sample: [
        {
            "account_description": "",
            "account_name": "demoaccount",
            "account_status": "Available",
            "account_type": "Normal",
            "database_privileges": {
                "database_privilege": []
            },
            "db_instance_id": "rm-dj13c34832w21g47j"
        },        
        {
            "account_description": "",
            "account_name": "testaccount",
            "account_status": "Available",
            "account_type": "Normal",
            "database_privileges": {
                "database_privilege": []
            },
            "db_instance_id": "rm-dj13c34832w21g47j"
        }
    ]
total:
    description: The number of all rds accounts.
    returned: when success
    type: int
    sample: 2
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
        db_instance_id=dict(type='str', required=True),
        account_names=dict(type='list', aliases=['names'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json("Package 'footmark' required for this module.")

    # Get values of variable
    db_instance_id = module.params['db_instance_id']
    names = module.params['account_names']
    result = []

    try:
        rds = rds_connect(module)

        if names and (not isinstance(names, list) or len(names)) < 1:
            module.fail_json(msg='account_name should be a list of account name, aborting')

        # fetch rds accounts by name
        if names:
            for name in names:
                rds_accounts = rds.list_account(db_instance_id=db_instance_id, account_name=name)
                if rds_accounts and len(rds_accounts) == 1:
                    result.append(get_info(rds_accounts[0]))

        # fetch all rds accounts
        else:
            names = []
            for account in rds.list_account(db_instance_id=db_instance_id):
                names.append(account.account_name)
                result.append(get_info(account))

        module.exit_json(changed=False, account_names=names, rds_accounts=result, total=len(result))
    except Exception as e:
        module.fail_json(msg="Unable to describe rds accounts, and got an error: {0}.".format(e))


if __name__ == "__main__":
    main()

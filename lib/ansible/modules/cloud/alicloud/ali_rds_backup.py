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
module: ali_rds_backup
version_added: "2.9"
short_description: Create, Delete rds backup in Alibaba Cloud..
description:
  - This module allows the user to manage rds backup. Includes support for creating, deleting.
  - Idempotence is not supported when creating backup sets
options:
  state:
    description:
      - If I(state=present), backup will be created.
      - If I(state=absent), backup will be removed.       
    default: present
    choices: ['present', 'absent']
    type: str
  db_instance_id:
    description:
      - Id of rds instance.
    aliases: ['instance_id']
    required: true
    type: str
  db_name:
    description:
      - The list of databases. Separate multiple databases with commas (,).
    type: list
  backup_id:
    description:
      - The ID of the backup set. Separate multiple values with commas (,). Up to 100 values can be entered in a single request
        Required when C(state=absent)
    type: list
  backup_method:
    description:
      - The backup type. Note Set Physical option when backing up a MariaDB snapshot.
        Logical backups can be performed only when the instance exists in a database.
    default: Physical
    type: str
  backup_strategy:
    description:
      - The backup policy. Valid values(db, instance). Note This parameter can be entered when MySQL logical backups or full physical backups for SQL Server are performed.
    type: str
  backup_type:
    description:
      - The backup method. Valid values(Auto, FullBackup)
    default: Auto
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
# basic provisioning example to operate backup
- name: Changed. Create backup
  ali_rds_backup:
    db_instance_id: '{{ db_instance_id }}'
    backup_method: Logical
    state: present
  register: bk

- name: Changed. Delete backup
  ali_rds_backup:
    db_instance_id: '{{ db_instance_id }}'
    backup_id: bk.backup.id
    state: absent
"""

RETURN = '''
backup:
    description: backup info.
    returned: when success
    type: complex
    contains:
        backup_id:
            description: The ID of the backup set.
            returned: always
            type: string
            sample: 321020562
        db_instance_id:
            description: The ID of the instance.
            returned: always
            type: string
            sample: rm-uf6wjk5xxxxxxx
        backup_status:
            description: The status of the backup set.
            returned: always
            type: string
            sample: Success
        backup_type:
            description: The backup type.
            returned: always
            type: string
            sample: FullBackup
        backup_mode:
            description: The backup mode.
            returned: always
            type: string
            sample: Automated
        backup_method:
            description: The ID of the instance.
            returned: always
            type: string
            sample: Physical
        status:
            description: alias of backup_status.
            returned: always
            type: string
            sample: Success
        id:
            description: alias of backup_id.
            returned: always
            type: string
            sample: 321020562
        instance_id:
            description: alias of db_instance_id.
            returned: always
            type: string
            sample: rm-uf6wjk5xxxxxxx
        backup_start_time:
            description: The start time of the current backup.
            returned: always
            type: string
            sample: 2019-12-17T01:51:13Z
        backup_end_time:
            description: The end time of the current backup.
            returned: always
            type: string
            sample: 2019-12-17T01:52:36Z
        backup_intranet_download_url:
            description: The download link for the private network access. If the download is unavailable, this parameter is a null string.
            returned: always
            type: string
            sample: http://rdsbak-bj-v4.oss-cn-beijing-internal.aliyuncs.com/xxxxx
        backup_size:
            description: The size of the backup file. Unit Byte.
            returned: always
            type: string
            sample: 10240
'''
notes = """
    - Idempotence is not supported when creating backup sets
"""

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
        db_instance_id=dict(type='str', aliases=['instance_id'], required=True),
        db_name=dict(type='list'),
        backup_id=dict(type='list'),
        backup_method=dict(type='str', default='Physical'),
        backup_strategy=dict(type='str'),
        backup_type=dict(type='str', default='Auto')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    rds = rds_connect(module)

    if HAS_FOOTMARK is False:
        module.fail_json("Footmark required for this module")

    # Get values of variable
    state = module.params['state']
    backup_id = module.params['backup_id']
    db_name = module.params['db_name']
    if backup_id:
        module.params['backup_id'] = ','.join(backup_id)
    if db_name:
        module.params['db_name'] = ','.join(db_name)

    if state == 'absent':
        try:
            changed = rds.delete_backup(**module.params)
            module.exit_json(changed=changed, backup={})
        except Exception as e:
            module.fail_json(msg=str("Unable to delete backup error:{0}".format(e)))

    if state == 'present':
        try:
            create_backup = rds.create_backup(**module.params)
            module.exit_json(changed=True, backup=create_backup.read())
        except Exception as e:
            module.fail_json(msg=str("Unable to create backup error:{0}".format(e)))


if __name__ == "__main__":
    main()

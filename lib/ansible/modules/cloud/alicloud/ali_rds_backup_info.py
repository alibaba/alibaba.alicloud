#!/usr/bin/python
# -*- coding: utf-8 -*-

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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_rds_backup_info
version_added: "2.9"
short_description: Gather info on backup of Alibaba Cloud.
description:
     - Gather info on backup of Alibaba Cloud and Support to use id, status, mode to filter backup.
options:
    db_instance_id:
      description:
        - Id of rds instance.
      aliases: ["instance_id"]
      type: str
    backup_id:
      description:
        - The ID of the backup set.
      type: str
    backup_status:
      description:
        - The status of the backup.
      type: str
    backup_mode:
      description:
        - The backup mode.
      type: str  
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.16.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch backup according to setting different filters
- name: Get the existing backup with backup_status
  ali_rds_backup_info:
    db_instance_id: '{{ db_instance_id }}'
    backup_status: Success

- name: Get the existing backup with backup_mode
  ali_rds_backup_info:
    db_instance_id: '{{ db_instance_id }}'
    backup_mode: Automated
        
'''

RETURN = '''
backups:
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
            description: alias of dbinstance_id.
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, rds_connect, vpc_connect

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
        backup_id=dict(type='str'),
        backup_status=dict(type='str', choice=['Success', 'Failed']),
        backup_mode=dict(type='str', choice=['Automated', 'Manual'])
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    result = []
    backup_status = module.params['backup_status']
    backup_mode = module.params['backup_mode']

    try:
        rds = rds_connect(module)
        for backup in rds.describe_backups(**module.params):
            if backup_status and backup.status.lower() != backup_status.lower():
                continue
            if backup_mode and backup.mode.lower() != backup_status.lower():
                continue
            result.append(backup.read())

    except Exception as e:
        module.fail_json(msg="Unable to describe rds backup, and got an error: {0}.".format(e))

    module.exit_json(changed=True, backups=result)


if __name__ == '__main__':
    main()

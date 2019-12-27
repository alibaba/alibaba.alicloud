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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_rds_backup_policy_info
version_added: "2.9"
short_description: Gather info on rds instance backup policy of Alibaba Cloud.
description:
     - Gather info on rds instance backup policy of Alibaba Cloud.
options:
    db_instance_id:
      description:
        - Id of rds instance.
      aliases: ["instance_id"]
      required: True
    backup_policy_mode:
      description:
        - The type of the backup.
      choice: ['DataBackupPolicy', 'LogBackupPolicy'],
    compress_type:
      description:
        - The compression method. This parameter is valid only when you change the compression method to QuickLZ for an RDS MySQL 5.6 instance. 
          The backup data can be used to restore database tables. Value 4.
      choices: ['1', '4', '8']  
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
- name: Get the rds instance backup policy.
  ali_rds_policy_info:
    db_instance_id: '{{ db_instance_id }}'
    compress_type: 0
    backup_policy_mode: DataBackupPolicy 
'''
RETURN = '''
policy:
    description: policy info.
    returned: when success
    type: complex
    contains:
        backup_retention_period:
            description: The retention period of the data backup.
            returned: always
            type: int
            sample: 7
        preferred_backup_time:
            description: The data backup time. Format: HH:mmZ-HH:mmZ.
            returned: always
            type: string
            sample: 15:00Z-16:00Z		
        preferred_backup_period:
            description: The data backup period.
            returned: always
            type: string
            sample: Monday,Wednesday,Friday,Sunday
        backup_log:
            description: Indicates whether to enable log backups.
            returned: always
            type: string
            sample: Enable
        log_backup_retention_period:
            description: The retention period of the log backup.
            returned: always
            type: int
            sample: 7	
        duplication:
            description: Indicates whether to dump backup files to OSS.
            returned: always
            type: string
            sample: Enable
        duplication_content:
            description: Indicates whether to dump data backups or log backups to OSS.
            returned: always
            type: string
            sample: DATA
        duplication_location:
            description: The storage location of the backup file.
            returned: always
            type: complex
            contains: 
                location:
                    description: The location of duplication.
                    returned: always
                    type: complex
                    contains: 
                        bucket: 
                            description: The name of the target OSS bucket.
                            sample: mybucket
                            returned: always
                            type: string
                        endpoint:
                            description: The name of the endpoint.
                            sample: oss-cn-shanghai.aliyuncs.com
                            returned: always
                            type: string
                sotrage:
                    description: The storage media of the backup.
                    returned: always
                    type: string
                    sample: OSS
        enable_backup_log:
            description: Indicates whether to enable log backups.
            returned: always
            type: string
            sample: 1
        high_space_usage_protection:
            description: Indicates whether Binlogs must be deleted when the used space exceeds 80% or the remaining space is less than 5 GB.
            returned: always
            type: string
            sample: Enable
        local_log_retention_hours:
            description: The local retention hours of the log backup.
            returned: always
            type: int
            sample: 0 	
        local_log_retention_space:
            description: The maximum space utilization of the local log.
            returned: always
            type: string
            sample: 30	
        log_backup_frequency:
            description: The log backup frequency.
            returned: always
            type: string
            sample: LogInterval
        preferred_next_backup_time:
            description: The next backup time.
            returned: always
            type: string
            sample: 2018-01-19T15:15Z	
        compress_type:
            description: The compression method.
            returned: always
            type: string
            sample: 1	
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, rds_connect

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
        compress_type=dict(type='str', choices=['1', '4', '8']),
        backup_policy_mode=dict(type='str', aliases=['policy'], choices=['DataBackupPolicy', 'LogBackupPolicy']),
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    try:
        policy = rds_connect(module).describe_backup_policy(**module.params)
        module.exit_json(changed=False, policy=policy.read())
    except Exception as e:
        module.fail_json(msg="Unable to describe rds backup policy, and got an error: {0}.".format(e))


if __name__ == '__main__':
    main()

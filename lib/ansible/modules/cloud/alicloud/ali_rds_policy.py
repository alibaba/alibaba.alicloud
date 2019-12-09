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
module: ali_rds_policy
version_added: "2.9"
short_description: Modify rds instance backup policy in Alibaba Cloud..
description:
  - This module allows the user to modify rds instance backup policy.
options:
  db_instance_id:
    description:
      - Id of rds instance.
      - This is used to specify rds instance.
    aliases: ['instance_id']
    required: true
  backup_policy_mode:
    description:
      - The type of the backup.Valid values(DataBackupPolicy, LogBackupPolicy)
  preferred_backup_time:
    description:
      - The time when the backup task is performed. Required when C(backup_policy_mode=DataBackupPolicy)
    aliases: ['backup_time']
  preferred_backup_period:
    description:
      - The backup period. Separate multiple values with commas (,). Required when C(backup_policy_mode=DataBackupPolicy)
    aliases: ['backup_period']
  backup_retention_period:
    description:
      - The retention period of the data backup. Value range 7 to 730. The default value is the original value. Required when C(backup_policy_mode=LogBackupPolicy)
    aliases: ['backup_period']
  backup_log:
    description:
      - Indicates whether to enable log backups. Valid values: Enable | Disabled. The default value is the original value.
        Required when C(backup_policy_mode=DataBackupPolicy)         
    choices: ['Enable', 'Disabled']
  log_backup_retention_period:
    description:
      - The retention period of the log backup. Value range 7 to 730. It cannot be greater than the retention period of the data backup.
        Required when C(backup_log=Enable)  
        Note When you enable log backups, you can set the retention period of log backup files. This operation is applicable only to the following instances: MySQL, PostgreSQL, and PPAS.
  enable_backup_log:
    description:
      - Indicates whether to enable log backups. Required when C(backup_policy_mode=LogBackupPolicy) 
  local_log_retention_hours:
    description:
      - The local retention hours of the log backup. Value range(0 to 7)*24. The value 0 indicates that log backups are not retained locally. The default value is the original value.
        Required when C(backup_policy_mode=LogBackupPolicy)
    aliases=['log_retention_hours']
  local_log_retention_space:
    description:
      - The maximum cycle space utilization of the local log. If the maximum value of this parameter is exceeded, 
        you can start to delete the first Binlog until the space utilization is less than this ratio. Value range 0 to 50. 
        The default value is the original value. Required when C(backup_policy_mode=LogBackupPolicy)
    aliases=['log_retention_space']
  high_space_usage_protection:
    description:
      - Indicates whether to delete Binlogs unconditionally when the used space exceeds 80% or the remaining space is less than 5 GB. 
        Valid values Enable | Disable. The default value is the original value.
    choices: ['Enable', 'Disabled']
  log_backup_frequency:
    description:
      - The log backup frequency. Valid values LogInterval(Logs are backed up every 30 minutes).
        It is the same as the data backup frequency by default. 
      - Note The LogInterval parameter is applicable only to SQL Server instances.
  compress_type:
    description:
      - The compression method. This parameter is valid only when you change the compression method to QuickLZ for an RDS MySQL 5.6 instance. 
        The backup data can be used to restore database tables. Value 4.
    choices: ['1', '4', '8']  
  archive_backup_retention_period:
    description:
      - The number of days to keep archived backups. The default is 0, which means that archive backup is not turned on. 
        Value 30 ~ 1095.
  archive_backup_keep_count:
    description:
      - The number of archive backups to keep. The default is 1. Value When ArchiveBackupKeepPolicy is ByMonth, the value ranges from 1 to 31.
        When ArchiveBackupKeepPolicy is ByWeek, the value ranges from 1 to 7.
        Required when C(archive_backup_keep_policy!=KeepAll)  
  archive_backup_keep_policy:
    description:
      - The retention period of archive backups. The number of backups that can be saved in this period is determined by ArchiveBackupKeepCount. Default is 0
    choices: ['ByMonth', 'ByWeek', 'KeepAll']
author:
  - "Li Xue"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.16.0"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
# basic provisioning example to operate backup
- name: Changed. Modify backup policy.
  ali_rds_backup:
    db_instance_id: '{{ db_instance_id }}'
    backup_policy_mode: DataBackupPolicy
    preferred_backup_time: 00:00Z-01:00Z
    preferred_backup_period: [Wednesday, Saturday]
    backup_log: Enable
    log_backup_retention_period: 7
    compress_type: 1
    archive_backup_keep_count: 2
    archive_backup_keep_policy: ByMonth
    high_space_usage_protection: Enable
"""

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
                            sample: bucket
                            returned: always
                            type: string
                        endpoint:
                            description: The name of the endpoint.
                            sample: oss-cn-shanghai.aliyuncs.com
                            returned: always
                            type: string
                sotrage:
                    description: The storage media of the backup..
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
        backup_policy_mode=dict(type='str', aliases=['policy'], choices=['DataBackupPolicy', 'LogBackupPolicy']),
        preferred_backup_time=dict(type='str', aliases=['backup_time']),
        preferred_backup_period=dict(type='list', aliases=['backup_period']),
        backup_retention_period=dict(type='str', aliases=['retention_period']),
        backup_log=dict(type='str', choices=['Enable', 'Disabled']),
        log_backup_retention_period=dict(type='str', aliases=['log_retention_period']),
        enable_backup_log=dict(type='bool'),
        local_log_retention_hours=dict(type='str', aliases=['log_retention_hours']),
        local_log_retention_space=dict(type='str', aliases=['log_retention_space']),
        high_space_usage_protection=dict(type='str', choices=['Enable', 'Disabled']),
        log_backup_frequency=dict(type='str'),
        compress_type=dict(type='str', choices=['1', '4', '8']),
        archive_backup_retention_period=dict(type='str'),
        archive_backup_keep_count=dict(type='str'),
        archive_backup_keep_policy=dict(type='str', choices=['ByMonth', 'ByWeek', 'KeepAll'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    rds = rds_connect(module)

    if HAS_FOOTMARK is False:
        module.fail_json("Footmark required for this module")

    # Get values of variable
    preferred_backup_period = module.params['preferred_backup_period']

    if preferred_backup_period:
        module.params['preferred_backup_period'] = ','.join(preferred_backup_period)
    try:
        policy = rds.modify_backup_policy(**module.params)
        module.exit_json(changed=True, policy=policy.read())
    except Exception as e:
        module.fail_json(msg=str("Unable to edit backup policy error:{0}".format(e)))


if __name__ == "__main__":
    main()

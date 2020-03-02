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
module: ali_disk_info
version_added: "1.5.0"
short_description: Gather facts on disks of Alibaba Cloud ECS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the ECS disk itself.
options:
    zone_id:
      description:
        - Aliyun availability zone ID in which to launch the disk
      aliases: ['alicloud_zone', 'zone' ]
    disk_names:
      description:
        - A list of ECS disk names.
      aliases: ["names"]
    disk_ids:
      description:
        - A list of ECS disk ids.
      aliases: ["ids"]
    name_prefix:
      description:
        - Use a disk name prefix to filter disks.
    instance_id:
      description:
        - Filter the results by the specified ECS instance ID.
    encrypted:
      description:
        - Indicate whether the disk is encrypted or not.
      default: False
      type: bool
    resource_group_id:
      description:
        - The Id of resource group which the disk belongs.
      aliases: ["group_id"]
    category:
      description:
        - The category of disk.
      choices: ['cloud', 'cloud_efficiency', 'cloud_ssd', 'cloud_essd', 'local_ssd_pro', 'local_hdd_pro', 'ephemeral', 'ephemeral_ssd']
    disk_type:
      description:
        - The type of disk.
      choices: ["system", "data"]
      aliases: ["type"]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.19.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch disk details according to setting different filters
- name: Filter disk using disk_ids
  ali_disk_info:
    disk_ids: ['d-2ze3carakr2qxxxxxx', 'd-2zej6cuwzmummxxxxxx']

- name: Filter disk using name_prefix
  ali_disk_info:
    name_prefix: 'YourDiskName'

- name: Filter disk using zone id
  ali_disk_info:
    zone_id: 'cn-beijing-c'

- name: Filter all disks
  ali_disk_info:

- name: Filter disk using insatnce id
  ali_disk_info:
    instance_id: 'i-2zeii6c3xxxxxxx'
'''

RETURN = '''
disk_ids:
    description: List all disk's id after operating ecs disk.
    returned: when success
    type: list
    sample: ["d-2ze8ohezcyvm4omrabud","d-2zeakwizkdjdu4q4lfco"]
disks:
    description: Details about the ecs disks that were created.
    returned: when success
    type: list
    sample: [
    {
        "attached_time": "2017-08-15T06:47:55Z",
        "category": "cloud_efficiency",
        "creation_time": "2017-08-15T06:47:45Z",
        "delete_auto_snapshot": false,
        "delete_with_instance": true,
        "description": "helloworld",
        "detached_time": "",
        "device": "/dev/xvda",
        "disk_charge_type": "PostPaid",
        "enable_auto_snapshot": true,
        "encrypted": false,
        "id": "d-2ze8ohezcyvm4omrabud",
        "image_id": "ubuntu_140405_32_40G_cloudinit_20161115.vhd",
        "instance_id": "i-2zegc3s8ihxq2pcysekk",
        "name": "test1",
        "operation_locks": {
            "operation_lock": []
        },
        "portable": false,
        "product_code": "",
        "region_id": "cn-beijing",
        "size": 40,
        "snapshop_id": "",
        "status": "in_use",
        "type": "system",
        "zone_id": "cn-beijing-a"
    },
    {
        "attached_time": "2017-08-13T06:57:37Z",
        "category": "cloud_efficiency",
        "creation_time": "2017-08-13T06:57:30Z",
        "delete_auto_snapshot": false,
        "delete_with_instance": true,
        "description": "",
        "detached_time": "",
        "device": "/dev/xvda",
        "disk_charge_type": "PostPaid",
        "enable_auto_snapshot": true,
        "encrypted": false,
        "id": "d-2zeakwizkdjdu4q4lfco",
        "image_id": "ubuntu_140405_64_40G_cloudinit_20161115.vhd",
        "instance_id": "i-2zeenj8meljkoi85lz3c",
        "name": "test2",
        "operation_locks": {
            "operation_lock": []
        },
        "portable": false,
        "product_code": "",
        "region_id": "cn-beijing",
        "size": 40,
        "snapshop_id": "",
        "status": "in_use",
        "type": "system",
        "zone_id": "cn-beijing-a"
    }
]
total:
    description: The number of all disks after operating ecs disk.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        zone_id=dict(aliases=['zone', 'alicloud_zone']),
        disk_ids=dict(type='list', aliases=['ids']),
        disk_names=dict(type='list', aliases=['names']),
        name_prefix=dict(type='str'),
        instance_id=dict(type='str'),
        encrypted=dict(type='bool', default=False),
        resource_group_id=dict(type='str', aliases=['group_id']),
        category=dict(type='str', choices=['cloud', 'cloud_efficiency', 'cloud_ssd', 'cloud_essd', 'local_ssd_pro', 'local_hdd_pro', 'ephemeral', 'ephemeral_ssd']),
        disk_type=dict(type='str', choices=["system", "data"], aliases=['type'])
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)
    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module')

    ecs = ecs_connect(module)

    disks = []
    disk_ids = []
    ids = module.params['disk_ids']
    names = module.params['disk_names']
    if ids and (not isinstance(ids, list) or len(ids)) < 1:
        module.fail_json(msg='disk_ids should be a list of disk id, aborting')

    if names and (not isinstance(names, list) or len(names)) < 1:
        module.fail_json(msg='disk_names should be a list of disk name, aborting')

    name_prefix = module.params['name_prefix']
    if names:
        for name in names:
            module.params['disk_name'] = name
            for disk in ecs.describe_disks(**module.params):
                if name_prefix and not str(disk.name).startswith(name_prefix):
                    continue
                disks.append(disk.read())
                disk_ids.append(disk.id)
    else:
        for disk in ecs.describe_disks(**module.params):
            if name_prefix and not str(disk.name).startswith(name_prefix):
                continue
            disks.append(disk.read())
            disk_ids.append(disk.id)

    module.exit_json(changed=False, disk_ids=disk_ids, disks=disks, total=len(disks))


if __name__ == '__main__':
    main()

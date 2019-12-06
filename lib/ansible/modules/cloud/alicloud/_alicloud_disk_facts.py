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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_disk_facts
version_added: "1.0.9"
short_description: Gather facts on disks of Alibaba Cloud ECS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the ECS disk itself.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix "ali" will be more concise.
  alternative: Use M(ali_disk_facts) instead.
options:
    alicloud_zone:
      description:
        - Aliyun availability zone ID in which to launch the disk
      aliases: ['zone_id', 'zone' ]
    disk_names:
      description:
        - A list of ECS disk names.
      aliases: [ "names"]
    disk_ids:
      description:
        - A list of ECS disk ids.
      aliases: ["ids"]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch disk details according to setting different filters
- name: fetch disk details example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    alicloud_zone: cn-beijing-a

  tasks:
    - name: Find all disks in the specified region
      alicloud_disk_facts:
        alicloud_zone: "{{ alicloud_zone }}"
        alicloud_region: "{{ alicloud_region }}"
      register: all_disks
    - name: Find all disks based on the specified ids
      alicloud_disk_facts:
        alicloud_zone: "{{ alicloud_zone }}"
        alicloud_region: "{{ alicloud_region }}"
        disk_ids:
          - "d-2ze8ohezcyvm4omrabud"
          - "d-2zeakwizkdjdu4q4lfco"
      register: disks_by_ids
    - name: Find all disks based on the specified names/name-prefixes
      alicloud_disk_facts:
        alicloud_zone: "{{ alicloud_zone }}"
        alicloud_region: "{{ alicloud_region }}"
        disk_ids:
          - "d-2ze8ohezcyvm4omrabud"
          - "d-2zeakwizkdjdu4q4lfco"
        disk_names:
          - "test1"
      register: disks_by_names

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
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_disk_info(disk):
    """
        Retrieves disk information from an disk
        ID and returns it as a dictionary
    """
    return {
        'id': disk.id,
        'region_id': disk.region_id,
        'zone_id': disk.zone_id,
        'status': disk.status,
        'name': disk.disk_name,
        'description': disk.description,
        'type': disk.type,
        'category': disk.category,
        'encrypted': disk.encrypted,
        'size': disk.size,
        'image_id': disk.image_id,
        'snapshop_id': disk.source_snapshot_id,
        'product_code': disk.product_code,
        'portable': disk.portable,
        'operation_locks': disk.operation_locks,
        'instance_id': disk.instance_id,
        "device": disk.device,
        "delete_with_instance": disk.delete_with_instance,
        "delete_auto_snapshot": disk.delete_auto_snapshot,
        "enable_auto_snapshot": disk.enable_auto_snapshot,
        "creation_time": disk.creation_time,
        "attached_time": disk.attached_time,
        "detached_time": disk.detached_time,
        "disk_charge_type": disk.disk_charge_type,
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        alicloud_zone=dict(aliases=['zone_id', 'zone']),
        disk_ids=dict(type='list', aliases=['ids']),
        disk_names=dict(type='list', aliases=['names']),
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
    zone_id = module.params['alicloud_zone']
    if ids and (not isinstance(ids, list) or len(ids)) < 1:
        module.fail_json(msg='disk_ids should be a list of disk id, aborting')

    if names and (not isinstance(names, list) or len(names)) < 1:
        module.fail_json(msg='disk_names should be a list of disk name, aborting')

    if names:
        for name in names:
            for disk in ecs.get_all_volumes(zone_id=zone_id, volume_ids=ids, volume_name=name):
                disks.append(get_disk_info(disk))
                disk_ids.append(disk.id)
    else:
        for disk in ecs.get_all_volumes(zone_id=zone_id, volume_ids=ids):
            disks.append(get_disk_info(disk))
            disk_ids.append(disk.id)

    module.exit_json(changed=False, disk_ids=disk_ids, disks=disks, total=len(disks))


if __name__ == '__main__':
    main()

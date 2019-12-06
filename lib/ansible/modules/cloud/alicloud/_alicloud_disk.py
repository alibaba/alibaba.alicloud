#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_disk
version_added: "1.0.9"
short_description: Create, Attach, Detach or Delete a disk in Alicloud ECS
description:
  - Creates and delete a ECS disk.starts, stops, restarts or terminates ecs instances.
  - Attach a disk to an ecs instance or detach a disk from it.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix "ali" will be more concise.
  alternative: Use M(ali_disk) instead.
options:
  state:
    description:
      - The state of operating ecs disk.
    default: 'present'
    choices:
      - ['present', 'absent']
  alicloud_zone:
    description:
      - Aliyun availability zone ID which to launch the disk
    required: true
    aliases: [ 'zone_id', 'zone' ]
  disk_name:
    description:
      - The name of ECS disk, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, ".", "_", or "-".
        It cannot begin with http:// or https://.
    aliases: [ 'name' ]
  description:
    description:
      - The description of ECS disk, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
    aliases: [ 'disk_description' ]
  disk_category:
    description:
      - The category to apply to the disk.
    default: 'cloud'
    aliases: ['volume_type', 'disk_type']
    choices: ['cloud', 'cloud_efficiency', 'cloud_ssd']
  size:
    description:
      - Size of disk (in GB) to create.
        'cloud' valid value is 5~2000; 'cloud_efficiency' or 'cloud_ssd' valid value is 20~32768.
    aliases: ['volume_size', 'disk_size']
  snapshot_id:
    description:
      - Snapshot ID on which to base the data disk.
        If this parameter is specified, the value of 'size' will be ignored. The actual created disk size is the specified snapshot's size.
    aliases: ['snapshot']
  disk_tags:
    description:
      - A list of hash/dictionaries of instance tags, ['{"tag_key":"value", "tag_value":"value"}'],
                tag_key must be not null when tag_value isn't null.
    aliases: ['tags']
  instance_id:
    description:
      - Ecs instance ID is used to attach the disk. The specified instance and disk must be in the same zone.
        If it is null or not be specified, the attached disk will be detach from instance.
    aliases: ['instance']
  disk_id:
    description:
      - Disk ID is used to attach an existing disk (required instance_id), detach or remove an existing disk.
    required: true
    aliases: ['vol_id', 'id']
  delete_with_instance:
    description:
      - When set to true, the disk will be released along with terminating ECS instance.
        When mark instance's attribution 'OperationLocks' as "LockReason":"security",
        its value will be ignored and disk will be released along with terminating ECS instance.
    aliases: ['delete_on_termination']
    type: bool
notes:
  - At present, when attach disk, system allocates automatically disk device according to default order from /dev/xvdb to /dev/xvdz.
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"

'''

EXAMPLES = '''
#
# Provisioning new disk
#

# Basic provisioning example create a disk
- name: create disk
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    alicloud_zone: cn-beijing-b
    size: 20
    state: present
  tasks:
    - name: create disk
      alicloud_disk:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        size: '{{ size }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# Advanced example with tagging and snapshot
- name: create disk
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hongkong
    alicloud_zone: cn-hongkong-b
    disk_name: disk_1
    description: data disk_1
    size: 20
    snapshot_id: xxxxxxxxxx
    disk_category: cloud_ssd
    state: present
  tasks:
    - name: create disk
      alicloud_disk:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        disk_name: '{{ disk_name }}'
        description: '{{ description }}'
        size: '{{ size }}'
        snapshot_id: '{{ snapshot_id }}'
        disk_category: '{{ disk_category }}'
        state: '{{ state }}'
      register: result
    - debug: var=result


# Example to attach disk to an instance
- name: attach disk to instance
  hosts: localhost
  connection: local
  vars:
    state: present
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: us-west-1
    instance_id: xxxxxxxxxx
    disk_id: xxxxxxxxxx
    delete_with_instance: no
  tasks:
    - name: Attach Disk to instance
      alicloud_disk:
        state: '{{ state }}'
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_id: '{{ instance_id }}'
        disk_id: '{{ disk_id }}'
        delete_with_instance: '{{ delete_with_instance }}'
      register: result
    - debug: var=result


# Example to detach disk from instance
- name: detach disk
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: us-west-1
    disk_id: xxxxxxxxxx
    state: present
  tasks:
    - name: detach disk
      alicloud_disk:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        id: '{{ disk_id }}'
        state: '{{ state }}'
      register: result
    - debug: var=result


# Example to delete disk
- name: detach disk
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: us-west-1
    disk_id: xxxxxxxxxx
    state: absent
  tasks:
    - name: detach disk
      alicloud_disk:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        disk_id: '{{ disk_id }}'
        state: '{{ state }}'
      register: result
    - debug: var=result
'''

RETURN = '''
device:
    description: device name of attached disk
    returned: except on delete
    type: string
    sample: "/def/xdva"
disk_category:
    description: the category of disk
    returned: except on delete
    type: string
    sample: "cloud"
disk_id:
    description: the id of disk
    returned: when success
    type: string
    sample: "d-2zecn395ktww53aylfw6 "
disk_status:
    description: the current status of disk
    returned: except on delete
    type: string
    sample: "available"
disk:
    description: Details about the ecs disk that was created.
    returned: except on delete
    type: dict
    sample: {
        "category": "cloud_efficiency",
        "description": "travis-ansible-instance",
        "device": "",
        "disk_name": "travis-ansible-instance",
        "id": "d-2ze9yw0a1sw9neyx8t24",
        "instance_id": "",
        "launch_time": "2017-06-19T03:19:30Z",
        "region_id": "cn-beijing",
        "size": 40,
        "status": "available",
        "type": "data",
        "zone_id": "cn-beijing-a"
    }
instance_id:
    description: the instance id which attached disk
    returned: on attach
    type: string
    sample: "i-i2rnfnenfnds"
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_disk_detail(disk):
    """
    Method call to attach disk

    :param module: Ansible module object
    :param disk_id:  ID of Disk to Describe
    :return: return id, status and object of disk
    """

    return {'id': disk.disk_id,
            'category': disk.category,
            'size': disk.size,
            'device': disk.device,
            'zone_id': disk.zone_id,
            'region_id': disk.region_id,
            'launch_time': disk.creation_time,
            'disk_name': disk.disk_name,
            'description': disk.description,
            'status': disk.status,
            'type': disk.type,
            'instance_id': disk.instance_id
            }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(),
        alicloud_zone=dict(aliases=['zone_id', 'zone']),
        state=dict(default='present', choices=['present', 'absent']),
        disk_id=dict(aliases=['vol_id', 'id']),
        disk_name=dict(aliases=['name']),
        disk_category=dict(aliases=['disk_type', 'volume_type']),
        size=dict(aliases=['disk_size', 'volume_size']),
        disk_tags=dict(type='list', aliases=['tags']),
        snapshot_id=dict(aliases=['snapshot']),
        description=dict(aliases=['disk_description']),
        instance_id=dict(aliases=['instance']),
        delete_with_instance=dict(aliases=['delete_on_termination'], default=None)
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_FOOTMARK:
        module.fail_json(msg="footmark required for the module alicloud_disk.")

    ecs = ecs_connect(module)
    state = module.params['state']

    instance_id = module.params['instance_id']
    disk_id = module.params['disk_id']
    zone_id = module.params['alicloud_zone']
    disk_name = module.params['disk_name']
    delete_with_instance = module.params['delete_with_instance']
    description = module.params['description']

    changed = False
    current_disk = None

    try:
        if disk_id:
            disks = ecs.get_all_volumes(zone_id=zone_id, volume_ids=[disk_id])
            if disks and len(disks) == 1:
                current_disk = disks[0]
        elif disk_name:
            disks = ecs.get_all_volumes(zone_id=zone_id, volume_name=disk_name)
            if disks:
                if len(disks) == 1:
                    current_disk = disks[0]
                else:
                    disk_ids = []
                    for d in disks:
                        disk_ids.append(d.id)
                    module.fail_json(msg="There is too many disks match name '{0}', "
                                         "please use disk_id or a new disk_name to specify a unique disk."
                                         "Matched disk ids are: {1}".format(disk_name, disk_ids))
    except ECSResponseError as e:
        module.fail_json(msg='Error in get_all_volumes: %s' % str(e))

    if state == 'absent':
        if not current_disk:
            module.fail_json(msg="Please use disk_id or disk_name to specify one disk for detaching or deleting.")
        if instance_id:
            try:
                changed = current_disk.detach(instance_id)
                module.exit_json(changed=changed, disk_id=current_disk.id, disk_category=current_disk.category,
                                 disk_status=current_disk.status, instance_id=instance_id,
                                 disk=get_disk_detail(current_disk))
            except Exception as e:
                module.fail_json(msg='Detaching disk {0} is failed, error: {1}'.format(current_disk.id, e))

        try:
            changed = current_disk.delete()
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='Deleting disk {0} is failed, error: {1}'.format(current_disk.id, e))

    # state == present
    if not current_disk:
        disk_category = module.params['disk_category']
        size = module.params['size']
        disk_tags = module.params['disk_tags']
        snapshot_id = module.params['snapshot_id']
        client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
        try:
            current_disk = ecs.create_disk(zone_id=zone_id, disk_name=disk_name,
                                           description=description, disk_category=disk_category, size=size,
                                           disk_tags=disk_tags, snapshot_id=snapshot_id, client_token=client_token)
            changed = True
        except Exception as e:
            module.fail_json(msg='Creating a new disk is failed, error: {0}'.format(e))

    else:
        try:
            if current_disk.name != disk_name \
                    or current_disk.description != description \
                    or current_disk.delete_with_instance != delete_with_instance:
                changed = current_disk.modify(disk_name=disk_name, description=description,
                                              delete_with_instance=delete_with_instance)
        except Exception as e:
            module.fail_json(msg='Updating disk {0} attribute is failed, error: {1}'.format(current_disk.id, e))

    if instance_id and current_disk and str(current_disk.status).lower() == "available":
        try:
            changed = current_disk.attach(instance_id=instance_id, delete_with_instance=delete_with_instance)
        except Exception as e:
            module.fail_json(
                msg='Attaching disk {0} to instance {1} is failed, error: {2}'.format(current_disk.id, instance_id, e))

    module.exit_json(changed=changed, disk_id=current_disk.id, disk_category=current_disk.category,
                     disk_status=current_disk.status, instance_id=instance_id, disk=get_disk_detail(current_disk))


if __name__ == '__main__':
    main()

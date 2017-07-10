#!/usr/bin/python
#
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: alicloud_disk
version_added: "2.4"
short_description: Create, Attach, Detach or Delete a disk in Alicloud ECS
description:
  - Creates and delete a ECS disk.starts, stops, restarts or terminates ecs instances.
  - Attach a disk to an ecs instance or detach a disk from it.
options:
  status:
    description: The state of operating ecs disk.
    required: false
    default: 'present'
    aliases: [ 'state' ]
    choices:
      - ['present', 'absent']
      - map operation ['create', 'attach', 'detach', 'delete']
  alicloud_zone:
    description: Aliyun availability zone ID which to launch the disk
    required: true
    default: null
    aliases: [ 'acs_zone', 'ecs_zone', 'zone_id', 'zone' ]
  disk_name:
    description:
      - The name of ECS disk, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, ".", "_", or "-".
        It cannot begin with http:// or https://.
    required: false
    default: null
    aliases: [ 'name' ]
  description:
    description:
      - The description of ECS disk, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
    required: false
    default: null
    aliases: [ 'disk_description' ]
  disk_category:
    description: The category to apply to the disk.
    required: false
    default: 'cloud'
    aliases: ['volume_type', 'disk_type']
    choices: ['cloud', 'cloud_efficiency', 'cloud_ssd']
  size:
    description:
      - Size of disk (in GB) to create.
        'cloud' valid value is 5~2000; 'cloud_efficiency' or 'cloud_ssd' valid value is 20~32768.
    required: false
    default: null
    aliases: ['volume_size', 'disk_size']
  snapshot_id:
    description:
      - Snapshot ID on which to base the data disk.
        If this parameter is specified, the value of 'size' will be ignored. The actual created disk size is the specified snapshot's size.
    required: false
    default: null
    aliases: ['snapshot']
  disk_tags:
    description:
      - A list of hash/dictionaries of instance tags, ['{"tag_key":"value", "tag_value":"value"}'],
                tag_key must be not null when tag_value isn't null.
    required: false
    default: null
    aliases: ['tags']
  instance_id:
    description:
      - Ecs instance ID is used to attach the disk. The specified instance and disk must be in the same zone.
        If it is null or not be specified, the attached disk will be detach from instance.
    required: false
    default: null
    aliases: ['instance']
  disk_id:
    description: Disk ID is used to attach an existing disk (required instance_id), detach or remove an existing disk.
    required: true
    default: null
    aliases: ['vol_id', 'id']
  delete_with_instance:
    description:
      - When set to "yes" or "true", the disk will be released along with terminating ECS instance.
        When mark instance's attribution 'OperationLocks' as "LockReason":"security",
        its value will be ignored and disk will be released along with terminating ECS instance.
    required: false
    default: none
    aliases: ['delete_on_termination']
    choices: ['yes/true', 'no/false']
notes:
  - At present, when attach disk, system allocates automatically disk device according to default order from /dev/xvdb to /dev/xvdz.
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
    status: present
  tasks:
    - name: create disk
      alicloud_disk:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        size: '{{ size }}'
        status: '{{ status }}'
      register: result
    - debug: var=result

# Advanced example with tagging and snapshot
- name: create disk
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    alicloud_zone: cn-hongkong-b
    disk_name: disk_1
    description: data disk_1
    size: 20
    snapshot_id: xxxxxxxxxx
    disk_category: cloud_ssd
    status: present
  tasks:
    - name: create disk
      alicloud_disk:
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        disk_name: '{{ disk_name }}'
        description: '{{ description }}'
        size: '{{ size }}'
        snapshot_id: '{{ snapshot_id }}'
        disk_category: '{{ disk_category }}'
        status: '{{ status }}'
      register: result
    - debug: var=result


# Example to attach disk to an instance
- name: attach disk to instance
  hosts: localhost
  connection: local
  vars:
    status: present
    alicloud_region: us-west-1
    instance_id: xxxxxxxxxx
    disk_id: xxxxxxxxxx
    delete_with_instance: no
  tasks:
    - name: Attach Disk to instance
      alicloud_disk:
        status: '{{ status }}'
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
    alicloud_region: us-west-1
    disk_id: xxxxxxxxxx
    status: present
  tasks:
    - name: detach disk
      alicloud_disk:
        alicloud_region: '{{ alicloud_region }}'
        id: '{{ disk_id }}'
        status: '{{ status }}'
      register: result
    - debug: var=result


# Example to delete disk
- name: detach disk
  hosts: localhost
  connection: local
  vars:
    alicloud_region: us-west-1
    disk_id: xxxxxxxxxx
    status: absent
  tasks:
    - name: detach disk
      alicloud_disk:
        alicloud_region: '{{ alicloud_region }}'
        disk_id: '{{ disk_id }}'
        status: '{{ status }}'
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_disks(module, ecs, disk_id):
    """
    Method call to attach disk

    :param module: Ansible module object
    :param disk_id:  ID of Disk to Describe
    :return: return id, status and object of disk
    """

    if not disk_id:
        module.fail_json(msg='disk_id is required for describing disk')

    disk_result = ecs.get_all_volumes(volume_ids=[disk_id])

    if 'error' in (''.join(str(disk_result))).lower():
        module.fail_json(disk_id=disk_id, msg='Retrieving disk got an error: {0}'.format(disk_result))

    disks = []
    for disk in disk_result:
        disks.append({'id': disk.disk_id,
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
                      })

    return disks


def create_disk(module, ecs, zone_id, disk_name, description,
                disk_category, size, disk_tags, snapshot_id):
    """
    create an disk in ecs
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param zone_id: ID of a zone to which an disk belongs.
    :param disk_name: Display name of the disk, which is a string
        of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain
        numerals, ".", "_", or "-".
    :param description: Description of the disk, which is a string of
        2 to 256 characters.
    :param disk_category: Displays category of the data disk
    :param size: Size of the system disk, in GB, values range
    :param disk_tags: A list of hash/dictionaries of instance
        tags, '[{tag_key:"value", tag_value:"value"}]', tag_key
        must be not null when tag_value isn't null
    :param snapshot_id: Snapshots are used to create the data disk
        After this parameter is specified, Size is ignored.
    :return: Returns a dictionary of disk information
    """

    changed = False
    if not zone_id:
        module.fail_json(msg='zone_id is required for new disk')

    try:
        changed, disk_id, result = ecs.create_disk(zone_id=zone_id, disk_name=disk_name,
                                                   description=description, disk_category=disk_category, size=size,
                                                   disk_tags=disk_tags, snapshot_id=snapshot_id)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(msg="Creating disk got an error: {0}".format(result))

        disks = get_disks(module=module, ecs=ecs, disk_id=disk_id)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to create disk, error: {0}'.format(e))

    return changed, result, disk_id, disks[0]


def attach_disk(module, ecs, disk_id, instance_id, delete_with_instance):
    """
    Method call to attach disk

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param disk_id:  ID of Disk to Detach
    :param instance_id:  ID of an instance for disk to be attached
    :param region_id: ID of Region
    :param device: device for attaching
    :param delete_with_instance: should the disk be deleted with instance
    :return: return status of operation
    """
    changed = False
    if not instance_id:
        module.fail_json(msg='instance_id is required to attach disk')

    if not disk_id:
        module.fail_json(msg='disk id is required to attach disk')

    if delete_with_instance:
        if delete_with_instance.strip().lower() == "true":
            delete_with_instance = delete_with_instance.strip().lower()
        elif delete_with_instance.strip().lower() == "false":
            delete_with_instance = delete_with_instance.strip().lower()
        elif delete_with_instance.strip().lower() == "yes":
            delete_with_instance = "true"
        elif delete_with_instance.strip().lower() == "no":
            delete_with_instance = "false"
        else:
            delete_with_instance = None

    if delete_with_instance:
        delete_with_instance = delete_with_instance.strip().lower()

    try:
        changed, result = ecs.attach_disk(disk_id=disk_id, instance_id=instance_id, delete_with_instance=delete_with_instance)
        if 'error' in (''.join(str(result))).lower():
            module.log(msg=str(result))
            module.fail_json(msg="Attaching disk {0} to instance {1} got an error: {2}".format(disk_id, instance_id, result))

        disks = get_disks(module, ecs, disk_id)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to attach disk {0} to instance {1}, error: {2}'.format(disk_id, instance_id, e))
    return changed, result, disks[0]


def detach_disk(module, ecs, disk_id):
    """
    Method call to detach disk

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param disk_id:  ID of Disk to Detach
    :return: return status of operation
    """
    changed = False
    if not disk_id:
        module.fail_json(msg='disk id is required to detach disk')

    try:
        changed, result, instance_id = ecs.detach_disk(disk_id=disk_id)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(msg="Detaching disk {0} from instance {1} got an error: {2}".format(instance_id, disk_id, result))

        disks = get_disks(module=module, ecs=ecs, disk_id=disk_id)
    except ECSResponseError as e:
        module.fail_json(msg='Unable to detach disk {0} from instance {1}, error: {2}'.format(instance_id, disk_id, e))

    return changed, result, instance_id, disks[0]


def delete_disk(module, ecs, disk_id):
    """
    Method to delete a disk

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param disk_id:  ID of Disk to be Deleted
    :return: return status of operation
    """
    changed = False
    if not disk_id:
        module.fail_json(msg='disk id is required to delete disk')
    try:
        changed, result = ecs.delete_disk(disk_id=disk_id)
        if 'error code' in (''.join(str(result))).lower():
            module.fail_json(msg="Deleting disk {0} got an error: {1}".format(disk_id, result))

    except ECSResponseError as e:
        module.fail_json(msg='Unable to delete disk {0}, error: {1}'.format(disk_id, e))

    return changed, result


def main():
    if not HAS_FOOTMARK:
        module.fail_json(msg="footmark required for this module")

    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(),
        alicloud_zone=dict(aliases=['zone_id', 'acs_zone', 'ecs_zone', 'zone', 'availability_zone']),
        status=dict(default='present', aliases=['state'], choices=['present', 'absent']),
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
    ecs = ecs_connect(module)
    status = module.params['status']

    instance_id = module.params['instance_id']
    disk_id = module.params['disk_id']

    if status == 'present':

        len_instance = 0
        len_disk = 0
        operation_flag = ''

        if instance_id:
            len_instance = len(instance_id.strip())

        if disk_id:
            len_disk = len(disk_id.strip())

        if not instance_id:
            if disk_id is None or len_disk == 0:
                operation_flag = 'present'
            elif disk_id is not None or len_disk > 0:
                operation_flag = 'detach'
        elif instance_id is not None or len_instance > 0:
            if disk_id is not None or len_disk > 0:
                operation_flag = 'attach'

        if operation_flag == '':
            module.fail_json(msg='To attach disk: instance_id and disk_id both parameters are required.'
                                 ' To detach disk: only disk_id is to be set.'
                                 ' To create disk: disk_id and instance_id both are not to be sent.',
                             instance_id=instance_id, disk_id=disk_id)

        if operation_flag == 'present':
            # create disk parameter values
            zone_id = module.params['alicloud_zone']
            disk_name = module.params['disk_name']
            description = module.params['description']
            disk_category = module.params['disk_category']
            size = module.params['size']
            disk_tags = module.params['disk_tags']
            snapshot_id = module.params['snapshot_id']
            # create disk parameter values end

            changed, result, disk_id, disk_dict = create_disk(module=module, ecs=ecs, zone_id=zone_id, disk_name=disk_name,
                                                              description=description, disk_category=disk_category,
                                                              size=size, disk_tags=disk_tags, snapshot_id=snapshot_id)

            module.exit_json(changed=changed, disk_id=disk_id, disk_category=disk_dict['category'],
                             disk_status=disk_dict['status'], instance_id=instance_id, disk=disk_dict)

        elif operation_flag == 'attach':

            delete_with_instance = module.params['delete_with_instance']

            changed, result, disk_dict = attach_disk(module, ecs, disk_id, instance_id, delete_with_instance)
            module.exit_json(changed=changed, device=disk_dict['device'], disk_id=disk_id, disk_category=disk_dict['category'],
                             disk_status=disk_dict['status'], instance_id=instance_id, disk=disk_dict)

        elif operation_flag == 'detach':
            # performing operation detach disk from instance
            # instance_id is to be retreived in call

            changed, result, instance_id, disk_dict = detach_disk(module=module, ecs=ecs, disk_id=disk_id)
            module.exit_json(changed=changed, disk_id=disk_id, disk_category=disk_dict['category'],
                             disk_status=disk_dict['status'], instance_id=instance_id, disk=disk_dict)

    elif status == 'absent':
        # performing operation delete disk

        changed, result = delete_disk(module=module, ecs=ecs, disk_id=disk_id)
        module.exit_json(changed=changed, disk_id=disk_id)

    else:
        module.fail_json(msg='The expected state: {0} and {1}, but got {2}.'.format("present", "absent", status))


if __name__ == '__main__':
    main()

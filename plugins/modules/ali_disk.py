#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. <xiaozhu36>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_disk
short_description: Create, Attach, Detach or Delete a disk in Alicloud ECS
description:
  - Creates and delete a ECS disk.starts, stops, restarts or terminates ecs instances.
  - Attach a disk to an ecs instance or detach a disk from it.
options:
  state:
    description:
      - The state of operating ecs disk.
    default: 'present'
    choices: ['present', 'absent']
    type: str
  alicloud_zone:
    description:
      - Aliyun availability zone ID in which to launch the disk.
      - Required when creating a disk except an ESSD regional disk
        (C(cloud_regional_disk_auto)).
    aliases: ['zone_id', 'zone']
    type: str
  disk_name:
    description:
      - The name of ECS disk, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, ".", "_", or "-".
        It cannot begin with http:// or https://.
    aliases: ['name']
    type: str
  description:
    description:
      - The description of ECS disk, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
    aliases: ['disk_description']
    type: str
  resource_group_id:
    description:
      - The Id  of group which disk belongs to.
    aliases: ['group_id']
    type: str
  disk_category:
    description:
      - The category to apply to the disk.
    default: 'cloud'
    aliases: ['volume_type', 'disk_type']
    choices: ['cloud', 'cloud_efficiency', 'cloud_ssd', 'cloud_essd', 'cloud_auto', 'cloud_essd_entry', 'cloud_regional_disk_auto', 'elastic_ephemeral_disk_standard', 'elastic_ephemeral_disk_premium']
    type: str
  size:
    description:
      - Size of disk (in GB) to create.
        'cloud' valid value is 5~2000; 'cloud_efficiency', 'cloud_essd' or 'cloud_ssd' valid value is 20~32768.
    aliases: ['volume_size', 'disk_size']
    type: int
  snapshot_id:
    description:
      - Snapshot ID on which to base the data disk.
        If this parameter is specified, the value of 'size' will be ignored. The actual created disk size is the specified snapshot's size.
    aliases: ['snapshot']
    type: str
  disk_tags:
    description:
      - A dictionary of tags to apply to the disk. C({"key":"value"}).
    aliases: ['tags']
    type: dict
  purge_tags:
    description:
      - Remove disk tags that are not declared in C(disk_tags).
      - When C(true), specify every tag that should remain on the disk.
    default: false
    type: bool
  bursting_enabled:
    description:
      - Whether burst performance is enabled for a supported disk.
      - When specified for an existing disk, updates C(BurstingEnabled) through C(ModifyDiskAttribute).
    type: bool
  performance_level:
    description:
      - Performance level for an ESSD disk.
    choices: ['PL0', 'PL1', 'PL2', 'PL3']
    type: str
  provisioned_iops:
    description:
      - Provisioned IOPS for a supported disk category.
    type: int
  multi_attach:
    description:
      - Whether the disk is created as a shared disk. This setting is immutable after creation.
    type: str
  delete_auto_snapshot:
    description:
      - Whether automatic snapshots are deleted when the disk is deleted.
      - Applied with C(ModifyDiskAttribute) after disk creation and for an existing disk.
    type: bool
  enable_auto_snapshot:
    description:
      - Whether automatic snapshots are enabled for the disk.
      - Applied with C(ModifyDiskAttribute) after disk creation and for an existing disk.
    type: bool
  encrypted:
    description:
      - Whether to encrypt the disk when it is created.
      - Disk encryption is immutable after creation.
    type: bool
  kms_key_id:
    description:
      - Customer-managed KMS key ID used to encrypt the disk.
      - Requires C(encrypted=true), and must not exceed 64 characters.
      - The CMK must be a symmetric key in the active state.
    type: str
  instance_id:
    description:
      - Ecs instance ID is used to attach the disk. The specified instance and disk must be in the same zone.
        If it is null or not be specified, the attached disk will be detach from instance.
    aliases: ['instance']
    type: str
  disk_id:
    description:
      - Disk ID is used to attach an existing disk (required instance_id), detach or remove an existing disk.
    required: true
    aliases: ['vol_id', 'id']
    type: str
  delete_with_instance:
    description:
      - When set to true, the disk will be released along with terminating ECS instance.
        When mark instance's attribution 'OperationLocks' as "LockReason":"security",
        its value will be ignored and disk will be released along with terminating ECS instance.
    aliases: ['delete_on_termination']
    default: False
    type: bool
notes:
    - At present, when attach disk, system allocates automatically disk device according to default order from /dev/xvdb to /dev/xvdz.
requirements:
    - "python >= 3.6"
    - "footmark >= 1.18.0"
extends_documentation_fragment:
    - alibaba.alicloud.alicloud
author:
    - "He Guimin (@xiaozhu36)"
'''

EXAMPLES = '''
# Advanced example with tagging and snapshot
- name: Create disk
  alibaba.alicloud.ali_disk:
    alicloud_zone: cn-beijing-h
    disk_name: Ansible-Disk
    description: Create From Ansible
    size: 20
    disk_category: 'cloud'
    disk_tags:
      Environment: production
      CostCenter: R0000000
    purge_tags: true

# Create an encrypted disk with a customer-managed CMK
- name: Create encrypted disk
  alibaba.alicloud.ali_disk:
    alicloud_zone: cn-beijing-h
    disk_name: Ansible-Encrypted-Disk
    size: 20
    disk_category: cloud_essd
    encrypted: true
    kms_key_id: key-xxxxxxxxxxxxxxxx
    resource_group_id: rg-xxxxxxxx
    performance_level: PL1
    multi_attach: Enabled
    delete_auto_snapshot: true
    enable_auto_snapshot: false


# Example to attach disk to an instance
- name: Attach disk to instance
  alibaba.alicloud.ali_disk:
    instance_id: xxxxxxxxxx
    disk_id: xxxxxxxxxx
    delete_with_instance: true

# Example to delete disk
- name: Delete disk
  alibaba.alicloud.ali_disk:
    id: xxxxxxxxxx
    state: absent


# Example to detach disk from instance
- name: Detach disk
  alibaba.alicloud.ali_disk:
    instance_id: xxxxxxxxxx
    disk_id: xxxxxxxxxx
    state: absent
'''

RETURN = '''
device:
    description: device name of attached disk
    returned: except on delete
    type: str
    sample: "/def/xdva"
disk_category:
    description: the category of disk
    returned: except on delete
    type: str
    sample: "cloud"
disk_id:
    description: the id of disk
    returned: when success
    type: str
    sample: "d-2zecn395ktwxxxxx"
disk_status:
    description: the current status of disk
    returned: except on delete
    type: str
    sample: "available"
resource_group_id:
    description: Resource group ID reported for the disk.
    returned: when ECS returns a resource group ID
    type: str
performance_level:
    description: Performance level reported for the disk.
    returned: when ECS returns a performance level
    type: str
multi_attach:
    description: Shared-disk setting reported for the disk.
    returned: when ECS returns a multi-attach setting
    type: str
delete_auto_snapshot:
    description: Whether automatic snapshots are deleted when the disk is deleted.
    returned: when ECS returns the setting
    type: bool
enable_auto_snapshot:
    description: Whether automatic snapshots are enabled for the disk.
    returned: when ECS returns the setting
    type: bool
bursting_enabled:
    description: Whether burst performance is enabled for the disk.
    returned: when ECS returns the setting
    type: bool
provisioned_iops:
    description: Provisioned IOPS reported for the disk.
    returned: when ECS returns a provisioned IOPS value
    type: int
encrypted:
    description: Whether the disk is encrypted.
    returned: except on delete
    type: bool
    sample: true
kms_key_id:
    description: Customer-managed KMS key ID reported for an encrypted disk.
    returned: when ECS returns a customer-managed key
    type: str
    sample: "key-xxxxxxxxxxxxxxxx"
disk:
    description: Details about the ecs disk that was created.
    returned: except on delete
    type: dict
    sample: {
        "category": "cloud_efficiency",
        "description": "travis-ansible-instance",
        "device": "",
        "disk_name": "travis-ansible-instance",
        "delete_auto_snapshot": true,
        "enable_auto_snapshot": false,
        "encrypted": true,
        "id": "d-2ze9yw0a1sw9neyx8t24",
        "instance_id": "",
        "launch_time": "2017-06-19T03:19:30Z",
        "kms_key_id": "key-xxxxxxxxxxxxxxxx",
        "multi_attach": "Enabled",
        "performance_level": "PL1",
        "resource_group_id": "rg-xxxxxxxx",
        "region_id": "cn-beijing",
        "size": 40,
        "status": "available",
        "type": "data",
        "zone_id": "cn-beijing-a"
    }
instance_id:
    description: the instance id which attached disk
    returned: on attach
    type: str
    sample: "i-i2rnfnenfnds"
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.alibaba.alicloud.plugins.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

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
            'instance_id': disk.instance_id,
            'encrypted': getattr(disk, 'encrypted', False),
            'kms_key_id': getattr(disk, 'kmskey_id', None),
            'resource_group_id': getattr(disk, 'resource_group_id', None),
            'performance_level': getattr(disk, 'performance_level', None),
            'multi_attach': getattr(disk, 'multi_attach', None),
            'delete_auto_snapshot': getattr(disk, 'delete_auto_snapshot', None),
            'enable_auto_snapshot': getattr(disk, 'enable_auto_snapshot', None),
            'bursting_enabled': getattr(disk, 'bursting_enabled', None),
            'provisioned_iops': getattr(disk, 'provisioned_iops', None)
            }


def disk_attribute_matches(disk, parameter, desired):
    current = getattr(disk, parameter, None)
    if isinstance(desired, bool) and isinstance(current, str):
        current = current.lower() == 'true'
    return current == desired


def reconcile_disk_tags(ecs, disk, tags, purge_tags):
    if not tags and not purge_tags:
        return False
    changed = False
    # Disk.tags in the Footmark version supported by this collection still
    # parses the legacy TagKey/TagValue spelling. Query the ECS tag API so
    # reconciliation uses the actual tag set returned by the service.
    current_tags = ecs.list_tag_resources(resource_ids=[disk.id], resource_type='disk') or {}
    if purge_tags:
        remove = {key: value for key, value in current_tags.items() if key not in tags}
        if remove and ecs.untag_resources(resource_ids=[disk.id], resource_type='disk', tags=remove):
            changed = True
    if tags and ecs.tag_resources(resource_ids=[disk.id], resource_type='disk', tags=tags):
        changed = True
    return changed


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        resource_group_id=dict(type='str', aliases=['group_id']),
        alicloud_zone=dict(type='str', aliases=['zone_id', 'zone']),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        disk_id=dict(type='str', aliases=['vol_id', 'id']),
        disk_name=dict(type='str', aliases=['name']),
        disk_category=dict(type='str', aliases=['disk_type', 'volume_type'], choices=['cloud', 'cloud_efficiency', 'cloud_ssd', 'cloud_essd', 'cloud_auto', 'cloud_essd_entry', 'cloud_regional_disk_auto', 'elastic_ephemeral_disk_standard', 'elastic_ephemeral_disk_premium'], default='cloud'),
        size=dict(type='int', aliases=['disk_size', 'volume_size']),
        disk_tags=dict(type='dict', aliases=['tags']),
        purge_tags=dict(type='bool', default=False),
        bursting_enabled=dict(type='bool', default=None),
        performance_level=dict(type='str', choices=['PL0', 'PL1', 'PL2', 'PL3']),
        provisioned_iops=dict(type='int'),
        multi_attach=dict(type='str'),
        delete_auto_snapshot=dict(type='bool', default=None),
        enable_auto_snapshot=dict(type='bool', default=None),
        encrypted=dict(type='bool', default=False),
        kms_key_id=dict(type='str'),
        snapshot_id=dict(type='str', aliases=['snapshot']),
        description=dict(type='str', aliases=['disk_description']),
        instance_id=dict(type='str', aliases=['instance']),
        delete_with_instance=dict(type='bool', aliases=['delete_on_termination'], default=False)
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_FOOTMARK:
        module.fail_json(msg="footmark required for the module ali_disk.")

    ecs = ecs_connect(module)
    state = module.params['state']

    instance_id = module.params['instance_id']
    disk_id = module.params['disk_id']
    zone_id = module.params['alicloud_zone']
    disk_name = module.params['disk_name']
    delete_with_instance = module.params['delete_with_instance']
    description = module.params['description']
    encrypted = module.params['encrypted']
    kms_key_id = module.params['kms_key_id']
    disk_tags = module.params['disk_tags'] or {}
    purge_tags = module.params['purge_tags']

    if kms_key_id and not encrypted:
        module.fail_json(msg='encrypted must be true when kms_key_id is specified')
    if kms_key_id and len(kms_key_id) > 64:
        module.fail_json(msg='kms_key_id must not exceed 64 characters')

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
        snapshot_id = module.params['snapshot_id']
        resource_group_id = module.params['resource_group_id']
        bursting_enabled = module.params['bursting_enabled']
        performance_level = module.params['performance_level']
        provisioned_iops = module.params['provisioned_iops']
        multi_attach = module.params['multi_attach']
        delete_auto_snapshot = module.params['delete_auto_snapshot']
        enable_auto_snapshot = module.params['enable_auto_snapshot']
        client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
        try:
            create_disk_args = dict(zone_id=zone_id, disk_name=disk_name,
                                    description=description, disk_category=disk_category, size=size,
                                    snapshot_id=snapshot_id, client_token=client_token)
            if disk_tags:
                # Footmark maps ``tags`` to CreateDiskRequest.set_Tags. Passing
                # the legacy ``disk_tags`` name silently drops the request field.
                create_disk_args['tags'] = disk_tags
            if encrypted:
                create_disk_args['encrypted'] = True
            if kms_key_id:
                create_disk_args['kms_key_id'] = kms_key_id
            if resource_group_id:
                create_disk_args['resource_group_id'] = resource_group_id
            if bursting_enabled is not None:
                create_disk_args['bursting_enabled'] = bursting_enabled
            if performance_level:
                create_disk_args['performance_level'] = performance_level
            if provisioned_iops is not None:
                create_disk_args['provisioned_iops'] = provisioned_iops
            if multi_attach:
                create_disk_args['multi_attach'] = multi_attach
            current_disk = ecs.create_disk(**create_disk_args)
            modify_disk_attribute_args = {'disk_id': current_disk.id}
            for parameter in ('delete_auto_snapshot', 'enable_auto_snapshot'):
                desired = module.params[parameter]
                if desired is not None and not disk_attribute_matches(current_disk, parameter, desired):
                    modify_disk_attribute_args[parameter] = desired
            if len(modify_disk_attribute_args) > 1:
                ecs.modify_disk_attribute(**modify_disk_attribute_args)
                # Footmark's Disk.update() passes the disk ID as the first
                # positional argument to get_all_volumes(), which is zone_id.
                # Refresh explicitly by volume_ids to avoid sending
                # ZoneId=[disk_id] to DescribeDisks.
                refreshed_disks = ecs.get_all_volumes(volume_ids=[current_disk.id])
                if refreshed_disks:
                    current_disk = refreshed_disks[0]
            changed = True
        except Exception as e:
            module.fail_json(msg='Creating a new disk is failed, error: {0}'.format(e))

    else:
        try:
            modify_disk_attribute_args = {'disk_id': current_disk.id}
            if disk_name and current_disk.name != disk_name:
                modify_disk_attribute_args['disk_name'] = disk_name
            if description is not None and current_disk.description != description:
                modify_disk_attribute_args['description'] = description
            if current_disk.delete_with_instance != delete_with_instance:
                modify_disk_attribute_args['delete_with_instance'] = delete_with_instance
            for parameter in ('delete_auto_snapshot', 'enable_auto_snapshot', 'bursting_enabled'):
                desired = module.params[parameter]
                if desired is not None and not disk_attribute_matches(current_disk, parameter, desired):
                    modify_disk_attribute_args[parameter] = desired
            if len(modify_disk_attribute_args) > 1:
                changed = ecs.modify_disk_attribute(**modify_disk_attribute_args)
        except Exception as e:
            module.fail_json(msg='Updating disk {0} attribute is failed, error: {1}'.format(current_disk.id, e))

    try:
        if reconcile_disk_tags(ecs, current_disk, disk_tags, purge_tags):
            changed = True
    except Exception as e:
        module.fail_json(msg='Updating disk {0} tags failed, error: {1}'.format(current_disk.id, e))

    if instance_id and current_disk and str(current_disk.status).lower() == "available":
        try:
            changed = current_disk.attach(instance_id=instance_id, delete_with_instance=delete_with_instance)
        except Exception as e:
            module.fail_json(
                msg='Attaching disk {0} to instance {1} is failed, error: {2}'.format(current_disk.id, instance_id, e))

    module.exit_json(changed=changed, disk_id=current_disk.id, disk_category=current_disk.category,
                     disk_status=current_disk.status, instance_id=instance_id,
                     encrypted=getattr(current_disk, 'encrypted', False),
                     kms_key_id=getattr(current_disk, 'kmskey_id', None),
                     resource_group_id=getattr(current_disk, 'resource_group_id', None),
                     performance_level=getattr(current_disk, 'performance_level', None),
                     multi_attach=getattr(current_disk, 'multi_attach', None),
                     delete_auto_snapshot=getattr(current_disk, 'delete_auto_snapshot', None),
                     enable_auto_snapshot=getattr(current_disk, 'enable_auto_snapshot', None),
                     bursting_enabled=getattr(current_disk, 'bursting_enabled', None),
                     provisioned_iops=getattr(current_disk, 'provisioned_iops', None),
                     disk=get_disk_detail(current_disk))


if __name__ == '__main__':
    main()

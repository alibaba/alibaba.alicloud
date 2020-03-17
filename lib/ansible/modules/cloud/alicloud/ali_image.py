#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com>
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_image
version_added: "2.9"
short_description: Create or delete user-defined image
description:
    - Create user-defined image from ECS instance, snapshot or disk_mapping; delete user-defined image 
options:
  state:
    description:
      - create or delete user-defined image
    default: 'present'
    choices: ['present', 'absent']
    type: str
  instance_id:
    description:
      - The ECS instance ID. A custom image is created from the specified instance.
    aliases: ['instance']
    type: str
  snapshot_id:
    description:
      - The system disk snapshot ID. A custom image is created from the specified snapshot.
    required: true   
    aliases: ['snapshot']
    type: str
  image_name:
    description:
      - The name of the image, [2, 128] English or Chinese characters.
        It must begin with an uppercase/lowercase letter or a Chinese character, and may contain numbers, "_" or "-".
        It cannot begin with http:// or https://.
    aliases: ['name']
    type: str
  description:
    description:
      - The description of the image, with a length limit of [0, 256] characters.
        Leaving it blank means null, which is the default value.
        It cannot begin with http:// or https://.
    type: str
  image_version:
    description:
      - The version number of the image, with a length limit of [1, 40] English characters.   
    aliases: ['version']
    type: str
  disk_mapping:
    description:
      - An optional list of device hashes/dictionaries with multiple snapshots configurations.
        It can combine multiple snapshots to be an image template.
    suboptions:
      snapshot_id:
        description:
          - The snapshot ID. Only one system disk's snapshot can be specified
      disk_size:
        description:
          - Size of the disk, in the range [5-2000GB]
    type: list 
  wait:
    description:
      - wait for the Image to be available.     
    type: bool
    default: False 
  wait_timeout:
    description:
      - how long before wait gives up, in seconds     
    default: 300
    type: int        
  image_id:
    description:
      - Image ID to be deregistered.
    type: str
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
'''

EXAMPLES = '''
# basic provisioning example to create image using ecs instance

- name: Create image form ecs instance
  ali_image:
    instance_id: '{{ instance_id }}'
  register: result

- name: Create image using snapshot
  ali_image:
    snapshot_id: '{{ snapshot_id }}'

- name: Create image using disk mapping
  ali_image:
    disk_mapping: '{{ disk_mapping }}'

- name: Create image with disk mapping and version
  ali_image:
    image_name: '{{ image_name }}'
    image_version: '{{ image_version }}'
    description: '{{ description }}'       
    disk_mapping: '{{ disk_mapping }}'
    wait: '{{ wait }}'
    wait_timeout: '{{ wait_timeout }}'

- name: delete image
  ali_image:
    image_id: '{{ image_id }}'
    state: 'absent'
'''

RETURN = '''
image:
    description: Details about the image that was created.
    returned: except on delete
    type: dict
    sample: {
        "disk_device_mappings": {
            "disk_device_mapping": [
                {
                    "device": "/dev/xvda",
                    "format": "",
                    "import_ossbucket": "",
                    "import_ossobject": "",
                    "size": "40",
                    "snapshot_id": "s-2zeddnvf7uhw3xw3its6",
                    "type": "system"
                }
            ]
        },
        "id": "m-2zee2i7regbnhhawrwc2",
        "image_name": "image_test",
        "launch_time": "2017-10-17T09:33:02Z",
        "platform": "CentOS",
        "region_id": "cn-beijing",
        "size": 40,
        "status": "Available"
    }
image_id:
    description: return the created image id
    returned: except on absent
    type: str
    sample: "m-2ze43t8c5urc4mvkx3fp"
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


def get_image_detail(image):
    """
    Method call to get image details
    :param image:  Image object to Describe
    :return: return id, status and object of disk
    """
    if image:
        return {'id': image.image_id,
                'image_name': image.image_name,
                'size': image.size,
                'region_id': image.region,
                'disk_device_mappings': image.disk_device_mappings,
                'status': image.status,
                'platform': image.platform,
                'launch_time': image.creation_time
                }


def create_image(module, ecs, snapshot_id, image_name, image_version, description, instance_id,
                 disk_mapping, client_token, wait, wait_timeout):
    """
    Create a user-defined image with snapshots.
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param snapshot_id: A user-defined image is created from the specified snapshot.
    :param image_name: image name which is to be created
    :param image_version: version of image
    :param description: description of the image
    :param instance_id: the specified instance_id
    :param disk_mapping: list relating device and disk
    :param client_token: Used to ensure the idempotence of the request
    :param wait: Used to indicate wait for instance to be running before running
    :param wait_timeout: Used to indicate how long to wait, default 300
    :return: id of image
    """
    changed = False
    if image_name:
        if len(image_name) < 2 or len(image_name) > 128:
            module.fail_json(msg='image_name must be 2 - 128 characters long')

        if image_name.startswith('http://') or image_name.startswith('https://'):
            module.fail_json(msg='image_name can not start with http:// or https://')
    if image_version:
        if image_version.isdigit():
            if int(image_version) < 1 or int(image_version) > 40:
                module.fail_json(msg='The permitted range of image_version is between 1 - 40')
        else:
            module.fail_json(msg='The permitted range of image_version is between 1 - 40, entered value is {0}'
                             .format(image_version))

    if disk_mapping:
        for mapping in disk_mapping:
            if mapping:
                if 'snapshot_id' not in mapping:
                    module.fail_json(msg='The snapshot_id of system disk is needed for disk mapping.')

                if not('disk_size' in mapping or 'snapshot_id' in mapping):
                    module.fail_json(msg='The disk_size and snapshot_id parameters '
                                         'are valid for disk mapping.')

                if 'disk_size' in mapping:
                    map_disk = mapping['disk_size']
                    if map_disk:
                        if str(map_disk).isdigit():
                            if int(map_disk) < 5 or int(map_disk) > 2000:
                                module.fail_json(msg='The permitted range of disk-size is 5 GB - 2000 GB ')
                        else:
                            module.fail_json(msg='The disk_size must be an integer value, entered value is {0}'.format(
                                map_disk))

    if not snapshot_id and not instance_id and not disk_mapping:
        module.fail_json(msg='Either of SnapshotId or InstanceId or disk_mapping, must be present for '
                             'create image operation to get performed')

    if (snapshot_id and instance_id) or (snapshot_id and disk_mapping) or (instance_id and disk_mapping):
        module.fail_json(msg='Only 1 of SnapshotId or InstanceId or disk_mapping, must be present for '
                             'create image operation to get performed')

    # call to create_image method in footmark
    try:
        changed, image_id, results, request_id = ecs.create_image(snapshot_id=snapshot_id, image_name=image_name,
                                                                  image_version=image_version, description=description,
                                                                  instance_id=instance_id, disk_mapping=disk_mapping,
                                                                  client_token=client_token, wait=wait,
                                                                  wait_timeout=wait_timeout)

        if 'error code' in str(results).lower():
            module.fail_json(changed=changed, msg=results)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to create image, error: {0}'.format(e))
    return changed, image_id, results, request_id


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        image_id=dict(type='str'),
        snapshot_id=dict(type='str', aliases=['snapshot']),
        description=dict(type='str'),
        image_name=dict(type='str', aliases=['name']),
        image_version=dict(type='str', aliases=['version']),
        disk_mapping=dict(type='list'),
        instance_id=dict(aliases=['instance']),
        state=dict(default='present', choices=['present', 'absent'], type='str'),
        wait=dict(default=False, type='bool'),
        wait_timeout=dict(type='int', default=300)
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_security_group.')

    ecs = ecs_connect(module)
    state = module.params['state']
    image_id = module.params['image_id']
    image_name = module.params['image_name']

    changed = False
    current_image = None

    try:
        if image_id:
            images = ecs.get_all_images(image_id=image_id)
            if images and len(images) == 1:
                current_image = images[0]
        elif image_name and state == 'absent':
            images = ecs.get_all_images(image_name=image_name)
            if images:
                if len(images) == 1:
                    current_image = images[0]
                else:
                    images_ids = []
                    for i in images:
                        images_ids.append(i.id)
                    module.fail_json(msg="There is too many images match name '{0}', "
                                         "please use image_id or a new image_name to specify a unique image."
                                         "Matched images ids are: {1}".format(image_name, images_ids))
        elif state == 'absent':
            images = ecs.get_all_images()
            if images and len(images) > 0:
                current_image = images[0]

    except ECSResponseError as e:
        module.fail_json(msg='Error in get_all_images: %s' % str(e))

    if state == 'absent':
        if not current_image:
            module.fail_json(msg="Please use valid image_id or image_name to specify one image for deleting.")

        try:
            changed_img = current_image.delete()
            module.exit_json(changed=changed_img, image_id=current_image.id, image=get_image_detail(current_image))
        except Exception as e:
            module.fail_json(msg='Deleting a image is failed, error: {0}'.format(e))
    if not current_image:
        snapshot_id = module.params['snapshot_id']
        image_version = module.params['image_version']
        description = module.params['description']
        disk_mapping = module.params['disk_mapping']
        instance_id = module.params['instance_id']
        wait = module.params['wait']
        wait_timeout = module.params['wait_timeout']


        try:
            # Calling create_image method
            client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
            changed, image_id, results, request_id = create_image(module=module, ecs=ecs, snapshot_id=snapshot_id,
                                                                  image_name=image_name, image_version=image_version,
                                                                  description=description, instance_id=instance_id,
                                                                  disk_mapping=disk_mapping, client_token=client_token,
                                                                  wait=wait, wait_timeout=wait_timeout)
            images = ecs.get_all_images(image_id=image_id)
            if images:
                if len(images) == 1:
                    current_image = images[0]

            module.exit_json(changed=changed, image_id=image_id, image=get_image_detail(current_image) )
        except Exception as e:
            module.fail_json(msg='Creating a new image is failed, error: {0}'.format(e))


if __name__ == '__main__':
    main()
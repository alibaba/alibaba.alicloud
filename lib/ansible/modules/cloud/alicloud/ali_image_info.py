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
module: ali_image_info
version_added: "2.9"
short_description: Gather facts on images of Alibaba Cloud ECS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the ECS image itself.

options:
    image_ids:
      description:
        - A list of ECS image ids.
      aliases: ["ids"]
      type: list
    image_names:
      description:
        - A list of ECS image names.
      aliases: ["names"]
      type: list
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch disk details according to setting different filters
- name: Find all images in the specified region
  ali_image_info:

- name: Find all images in the specified region by image ids
  ali_image_info:
    image_ids: '{{ image_ids }}'

- name: Find all images in the specified region by image names
  ali_image_info:
    image_names: '{{ image_names }}'
'''

RETURN = '''
image_ids:
    description: List all image's id after operating ecs image.
    returned: when success
    type: list
    sample: ["m-2zeddnvf7uhw3xwcr6dl", "m-2zeirrrgvh8co3z364f0"]
images:
    description: Details about the ecs images.
    returned: when success
    type: list
    sample: [
        {
            "architecture": "x86_64",
            "creation_time": "2019-03-27T09:47:10Z",
            "description": "",
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
            "image_id": "m-2zeddnvf7uhw3xwcr6dl",
            "image_name": "test_image_1",
            "image_owner_alias": "self",
            "image_version": "",
            "is_copied": false,
            "is_self_shared": "",
            "is_subscribed": false,
            "is_support_cloudinit": true,
            "is_support_io_optimized": true,
            "osname": "CentOS  7.3 64",
            "ostype": "linux",
            "platform": "CentOS",
            "product_code": "",
            "progress": "100%",
            "region": "cn-beijing",
            "size": 40,
            "status": "Available",
            "tags": {},
            "usage": "none"
        },
        {
            "architecture": "x86_64",
            "creation_time": "2019-03-27T09:47:10Z",
            "description": "",
            "disk_device_mappings": {
                "disk_device_mapping": [
                    {
                        "device": "/dev/xvda",
                        "format": "",
                        "import_ossbucket": "",
                        "import_ossobject": "",
                        "size": "80",
                        "snapshot_id": "s-2zeirrrgvh8co3z5nq5d",
                        "type": "system"
                    }
                ]
            },
            "image_id": "m-2zeirrrgvh8co3z364f0",
            "image_name": "test_image_2",
            "image_owner_alias": "self",
            "image_version": "",
            "is_copied": false,
            "is_self_shared": "",
            "is_subscribed": false,
            "is_support_cloudinit": true,
            "is_support_io_optimized": true,
            "osname": "CentOS  7.3 64",
            "ostype": "linux",
            "platform": "CentOS",
            "product_code": "",
            "progress": "100%",
            "region": "cn-beijing",
            "size": 80,
            "status": "Available",
            "tags": {},
            "usage": "instance"
        }
    ]
total:
    description: The number of all images after operating ecs image.
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


def get_info(image):
    """
        Retrieves image information from an image
        ID and returns it as a dictionary
    """
    return {
        'architecture': image.architecture,
        'creation_time': image.creation_time,
        'description': image.description,
        'disk_device_mappings': image.disk_device_mappings,
        'image_id': image.image_id,
        'image_name': image.image_name,
        'image_owner_alias': image.image_owner_alias,
        'image_version': image.image_version,
        'is_copied': image.is_copied,
        'is_self_shared': image.is_self_shared,
        'is_subscribed': image.is_subscribed,
        'is_support_cloudinit': image.is_support_cloudinit,
        'is_support_io_optimized': image.is_support_io_optimized,
        'platform': image.platform,
        'product_code': image.product_code,
        'progress': image.progress,
        "region": image.region,
        "size": image.size,
        "status": image.status,
        "tags": image.tags,
        "usage": image.usage,
        "osname": image.osname,
        "ostype": image.ostype
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        image_ids=dict(type='list', aliases=['ids']),
        image_names=dict(type='list', aliases=['names']),
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)
    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    image_ids = module.params['image_ids']
    image_names = module.params['image_names']
    result = []
    ids = []

    if image_ids and (not isinstance(image_ids, list) or len(image_ids)) < 1:
        module.fail_json(msg='image_ids should be a list of image id, aborting')

    if image_names and (not isinstance(image_names, list) or len(image_names)) < 1:
        module.fail_json(msg='image_names should be a list of image name, aborting')

    try:
        ecs = ecs_connect(module)
        if image_ids:
            image_id = ",".join(image_ids)
            for image in ecs.get_all_images(image_id=image_id):
                result.append(get_info(image))
                ids.append(image.image_id)

        elif image_names:
            for name in image_names:
                for image in ecs.get_all_images(image_name=name):
                    if image:
                        result.append(get_info(image))
                        ids.append(image.image_id)

        else:
            for image in ecs.get_all_images():
                result.append(get_info(image))
                ids.append(image.image_id)

        module.exit_json(changed=False, image_ids=ids, images=result, total=len(result))

    except ECSResponseError as e:
        module.fail_json(msg='Error in describe images: %s' % str(e))


if __name__ == '__main__':
    main()
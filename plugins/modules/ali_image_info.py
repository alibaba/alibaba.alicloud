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
module: ali_image_info
short_description: Gather facts on images of Alibaba Cloud ECS.
description:
     - This module fetches data from the Open API in Alicloud.
       Results include every page returned by C(DescribeImages).
     - C(image_names) accepts C(*) wildcards and ECS performs case-insensitive matching.
     - An empty query result is returned as an empty C(images) list; it is not retried indefinitely.

options:
    image_ids:
      description:
        - A list of ECS image ids.
        - Do not combine this option with C(image_names); image IDs take precedence when both are supplied.
      aliases: ["ids"]
      type: list
      elements: str
    image_names:
      description:
        - A list of ECS image names.
      aliases: ["names"]
      type: list
      elements: str
    filters:
      description:
        - Additional C(DescribeImages) request options, expressed in snake_case.
        - The module follows every API page; C(page_size) changes the number requested in each page, not the total result limit.
      type: dict
      suboptions:
        image_owner_alias:
          description:
            - Selects the image owner scope.
            - Set to C(marketplace) to query Marketplace images.
          type: str
        instance_type:
          description:
            - Returns images compatible with the specified ECS instance type.
          type: str
        os_type:
          description:
            - Filters images by operating system type, for example C(linux).
          type: str
        page_size:
          description:
            - Number of results requested from each C(DescribeImages) page.
            - Valid values are from C(1) to C(100); the default is C(100).
          type: int
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alibaba.alicloud.alicloud
'''

EXAMPLES = '''
# Fetch disk details according to setting different filters
- name: Find all images in the specified region
  alibaba.alicloud.ali_image_info:

- name: Find all images in the specified region by image ids
  alibaba.alicloud.ali_image_info:
    image_ids: '{{ image_ids }}'

- name: Find all images in the specified region by image names
  alibaba.alicloud.ali_image_info:
    image_names: '{{ image_names }}'

- name: Find Marketplace images by name
  alibaba.alicloud.ali_image_info:
    image_names:
      - 'Red Hat Enterprise Linux 9.6 64bit V*'
    filters:
      image_owner_alias: marketplace
      page_size: 100

# Golden Image flow: resolve a compatible source image, provision an instance, then create a tagged image.
- name: Resolve a Linux system image compatible with the requested instance type
  alibaba.alicloud.ali_image_info:
    filters:
      image_owner_alias: system
      instance_type: '{{ instance_type }}'
      os_type: linux
  register: compatible_images

- name: Create an encrypted build instance
  alibaba.alicloud.ali_instance:
    image_id: '{{ compatible_images.images[0].image_id }}'
    instance_type: '{{ instance_type }}'
    security_groups: ['{{ security_group_id }}']
    vswitch_id: '{{ vswitch_id }}'
    system_disk_encrypted: true
    system_disk_kms_key_id: '{{ kms_key_id }}'
    data_disks:
      - category: cloud_essd
        size: 40
        encrypted: true
        kms_key_id: '{{ kms_key_id }}'
    tags:
      Purpose: golden-image-build
  register: build_instance

- name: Create a tagged Golden Image
  alibaba.alicloud.ali_image:
    instance_id: '{{ build_instance.instances[0].id }}'
    image_name: ansible-golden-image
    tags:
      Purpose: golden-image
'''

RETURN = '''
image_ids:
    description: List all image's id after operating ecs image.
    returned: when success
    type: list
    sample: ["m-2zeddnvf7uhw3xwcr6dl", "m-2zeirrrgvh8co3z364f0"]
images:
    description: Details about the ECS images. C(product_code) identifies the Marketplace product and C(platform) identifies the operating system family.
    returned: when success
    type: list
    contains:
        image_id:
            description: ECS image ID.
            type: str
        image_owner_alias:
            description: Owner scope, for example C(self) or C(marketplace).
            type: str
        product_code:
            description: Marketplace product code when supplied by ECS.
            type: str
        platform:
            description: Operating system family reported by ECS.
            type: str
        tags:
            description: Image tags as key-value pairs.
            type: dict
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
from ansible_collections.alibaba.alicloud.plugins.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

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
        image_ids=dict(type='list', elements='str', aliases=['ids']),
        image_names=dict(type='list', elements='str', aliases=['names']),
        filters=dict(type='dict', default={}),
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)
    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    image_ids = module.params['image_ids']
    image_names = module.params['image_names']
    filters = module.params['filters']
    result = []
    ids = []

    if image_ids and (not isinstance(image_ids, list) or len(image_ids) < 1):
        module.fail_json(msg='image_ids should be a list of image id, aborting')

    if image_names and (not isinstance(image_names, list) or len(image_names) < 1):
        module.fail_json(msg='image_names should be a list of image name, aborting')

    try:
        ecs = ecs_connect(module)
        if image_ids:
            image_id = ",".join(image_ids)
            for image in ecs.get_all_images(image_id=image_id, filters=filters):
                result.append(get_info(image))
                ids.append(image.image_id)

        elif image_names:
            for name in image_names:
                for image in ecs.get_all_images(image_name=name, filters=filters):
                    if image:
                        result.append(get_info(image))
                        ids.append(image.image_id)

        else:
            for image in ecs.get_all_images(filters=filters):
                result.append(get_info(image))
                ids.append(image.image_id)

        module.exit_json(changed=False, image_ids=ids, images=result, total=len(result))

    except (ECSResponseError, ValueError) as e:
        module.fail_json(msg='Error in describe images: %s' % str(e))


if __name__ == '__main__':
    main()

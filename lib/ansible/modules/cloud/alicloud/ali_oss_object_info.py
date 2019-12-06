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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_oss_object_info
version_added: "1.5.0"
short_description: Gather facts on bucket objects of Alibaba Cloud OSS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the OSS bucket itself.
options:
    bucket:
        description:
          - OSS bucket name.  
    object:
        description:
          - Bucket object name.
        aliases: [ 'object_name' ]    
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch object details in the specified bucket
- name: List objects detail example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    bucket: xiaozhubucket
    object: newobject-1
  tasks:
    - name: List all objects in the specified bucket
      ali_oss_object_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        bucket: '{{ bucket }}'
      register: all_objects_in_bucket
    - debug: var=all_objects_in_bucket

    - name: List all objects that has the prefix of 'object' value in the specified bucket
      ali_oss_object_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        bucket: '{{ bucket }}'
        object: '{{ object }}'
      register: all_objects_by_name
    - debug: var=all_objects_by_name
'''

RETURN = '''
object_names:
    description: List all object's in the specified bucket
    returned: when success
    type: list
    sample: ["newobject-1", "newobject-2", "newobject-3"]
objects:
    description: The list all objects that has the prefix of 'object' value in the specified bucket
    returned: when list
    type: list
    sample: [
        {
            "etag": "64C63F0FCB9ABA4F74A3DF3A491BBC7A",
            "key": "newobject-1",
            "last_modified": "2017-10-26 15:18:38",
            "size": "1843 B",
            "storage_class": "Standard",
            "type": "Normal"
        },
        {
            "etag": "BE13E8EF0FB40070727817E1448345A0",
            "key": "newobject-2",
            "last_modified": "2017-10-26 15:18:38",
            "size": "15624 B",
            "storage_class": "Standard",
            "type": "Normal"
        },
        {
            "etag": "A7D40C705F555AD8B0A9557BBCCB1178",
            "key": "newobject-3",
            "last_modified": "2017-10-26 15:18:40",
            "size": "3541 B",
            "storage_class": "Standard",
            "type": "Normal"
        }
    ] 
total:
    description: The number of all object's in the specified bucket.
    returned: when success
    type: int
    sample: 3    
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_oss import oss_bucket_argument_spec, oss_bucket_connect
import time

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError, OSSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(obj):
    result = {
        'key': obj.key,
        'last_modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.last_modified)),
        'etag': obj.etag,
        'type': obj.type,
        'size': str(obj.size) + ' B',
        'storage_class': obj.storage_class
    }

    if obj.type == 'Appendable':
        result['next_append_position'] = obj.size

    return result


def main():
    argument_spec = oss_bucket_argument_spec()
    argument_spec.update(dict(
        bucket=dict(type='str', required=True),
        object=dict(type='str', aliases=['key', 'object_name']),
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    object_key = module.params['object']
    objects = []
    object_names = []
    max_keys = 500

    try:
        oss_bucket = oss_bucket_connect(module)

        while True:
            results = oss_bucket.list_objects(prefix=object_key, max_keys=max_keys)
            for obj in results:
                objects.append(get_info(obj))
                object_names.append(obj.key)

            if len(results) < max_keys:
                break
        module.exit_json(changed=False, object_names=object_names, objects=objects, total=len(objects))
    except Exception as e:
        module.fail_json(msg="Unable to describe bucket objects, and got an error: {0}".format(e))


if __name__ == '__main__':
    main()

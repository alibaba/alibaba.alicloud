#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_bucket_object
version_added: "2.5"
short_description: Manage object in OSS
description:
    - This module allows the user to manage OSS objects within bucket. Includes support for uploading and downloading
      objects, retrieving object keys.
options:
  mode:
    description:
      - Switches the module behaviour between put (upload), get (download), list (list objects) and delete (delete object).
    required: true
    choices: ['get', 'put', 'delete', 'list']
  bucket:
    description:
      - Bucket name.
    required: true
  permission:
    description:
      - This option lets the user set the canned permissions on the objects that are put. The permissions that
        can be set are 'private', 'public-read', 'public-read-write'.
    default: 'private'
    choices: [ 'private', 'public-read', 'public-read-write' ]
    aliases: [ 'acl' ]
  headers:
    description:
      - Custom headers for PUT or GET operation, as a dictionary of 'key=value' and 'key=value,key=value'.
  overwrite:
    description:
      - Force overwrite specified object content when putting object.
        If it is true/false, object will be normal/appendable. Appendable Object can be convert to Noraml by setting
        overwrite to true, but conversely, it won't be work.
    default: False
    type: bool
  content:
    description:
      - The object content that will be upload. It is conflict with 'file_name' when mode is 'put'.
  file_name:
    description:
      - The name of file that used to upload or download object.
    aliases: [ "file" ]
  object:
    description:
      - Name to object after uploaded to bucket
    required: true
    aliases: [ 'key', 'object_name' ]
  byte_range:
    description:
      - The range of object content that would be download.
        Its format like 1-100 that indicates range from one to hundred bytes of object.
    aliases: [ 'range' ]
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
'''

EXAMPLES = '''

# basic provisioning example to upload a content
- name: simple upload to bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    mode: put
    bucket: bucketname
    content: 'Hello world! I come from alicloud.'
    object: 'remote_file.txt'
    headers:
      Content-Type: 'text/html'
      Content-Encoding: md5
  tasks:
    - name: simple upload to bucket
      alicloud_bucket_object:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        content: '{{ content }}'
        headers: '{{ headers }}'
      register: result
    - debug: var=result

# basic provisioning example to upload a file
- name: simple upload to bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    mode: put
    bucket: bucketname
    file_name: 'test_oss.yml'
    object: 'remote_file.txt'
    headers:
      Content-Type: 'text/html'
      Content-Encoding: md5
  tasks:
    - name: simple upload to bucket
      alicloud_bucket_object:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        file_name: '{{ file_name }}'
        content: '{{ content }}'
        headers: '{{ headers }}'
      register: result
    - debug: var=result

# basic provisioning example to download a object
- name: simple upload to bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    mode: get
    bucket: bucketname
    download: 'my_test.json'
    byte_range: 0-100
    object: 'remote_file.txt'
    headers:
      Content-Type: 'text/html'
      Content-Encoding: md5
  tasks:
    - name: simple upload to bucket
      alicloud_bucket_object:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        file_name: '{{ download }}'
        byte_range: '{{ byte_range }}'
        content: '{{ content }}'
        headers: '{{ headers }}'
      register: result
    - debug: var=result

# basic provisioning example to list bucket objects
- name: list bucket objects
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    mode: list
    bucket: bucketname
  tasks:
    - name: list bucket objects
      alicloud_bucket_object:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
      register: list_result
    - debug: var=list_result

# basic provisioning example to delete bucket object
- name: delete bucket objects
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    mode: delete
    bucket: bucketname
    object: 'remote_file.txt'
  tasks:
    - name: delete bucket objects
      alicloud_bucket_object:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        object: '{{ object }}'
      register: delete_object_result
    - debug: var=delete_object_result
'''

RETURN = '''
changed:
    description: current operation whether changed the resource
    returned: when success
    type: bool
    sample: true
key:
    description: the name of oss object
    returned: expect list
    type: bool
    sample: true
object:
    description: the object's information
    returned: on put or get
    type: dict
    sample: {
        "etag": "A57B09D4A76BCF486DDD755900000000",
        "key": "newobject-2",
        "last_modified": "2017-07-24 19:43:41",
        "next_append_position": 11,
        "size": "11 B",
        "storage_class": "Standard",
        "type": "Appendable"
    }
objects:
    description: the list all objects that has the prefix of 'object' value in the specified bucket
    returned: when list
    type: list
    sample: [
        {
            "etag": "54739B1D5AEBFD38C83356D8A8A3EDFC",
            "key": "newobject-1",
            "last_modified": "2017-07-24 19:42:46",
            "size": "2788 B",
            "storage_class": "Standard",
            "type": "Normal"
        },
        {
            "etag": "EB8BDADA044D58D58CDE755900000000",
            "key": "newobject-2",
            "last_modified": "2017-07-24 19:48:28",
            "next_append_position": 5569,
            "size": "5569 B",
            "storage_class": "Standard",
            "type": "Appendable"
        }
    ]
'''
# import module snippets
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_oss import oss_bucket_argument_spec, oss_bucket_connect
import time

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError, OSSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_object_info(obj):
    result = {'key': obj.key, 'last_modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.last_modified)),
              'etag': obj.etag, 'type': obj.type, 'size': str(obj.size) + ' B', 'storage_class': obj.storage_class}

    if obj.type == 'Appendable':
        result['next_append_position'] = obj.size

    return result


def main():
    argument_spec = oss_bucket_argument_spec()
    argument_spec.update(dict(
        bucket=dict(type='str', required=True),
        mode=dict(type='str', required=True, choices=['put', 'get', 'list', 'delete']),
        permission=dict(type='str', default='private', choices=['private', 'public-read', 'public-read-write']),
        headers=dict(type='dict'),
        overwrite=dict(type='bool', default=False),
        content=dict(type='str'),
        file_name=dict(type='str', aliases=['file']),
        object=dict(type='str', aliases=['key', 'object_name']),
        byte_range=dict(type='str', aliases=['range'])
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_bucket_object.")

    oss_bucket = oss_bucket_connect(module)
    mode = module.params['mode']
    file_name = module.params['file_name']
    object_key = module.params['object']
    headers = module.params['headers']

    changed = False

    if mode == 'put':
        content = module.params['content']
        if content and file_name:
            module.fail_json(msg="'content' and 'file_name' only one can be specified when mode is put.")

        overwrite = module.params['overwrite']
        permission = module.params['permission']

        try:
            if content:
                oss_bucket.put_object(object_key, content, overwrite, headers=headers)
                changed = True
            elif file_name:
                oss_bucket.put_object_from_file(object_key, file_name, overwrite, headers=headers)
                changed = True
            elif oss_bucket.is_object_exist(object_key):
                if permission:
                    oss_bucket.put_object_acl(object_key, permission)
                    changed = True
                if headers:
                    oss_bucket.update_object_headers(object_key, headers)
                    changed = True
            module.exit_json(changed=changed, key=object_key, object=get_object_info(oss_bucket.get_object_info(object_key)))
        except Exception as e:
            module.fail_json(msg="Unable to upload an object {0} or "
                                 "modify its permission and headers, and got an error: {1}".format(object_key, e))

    elif mode == 'get':
        byte_range = module.params['byte_range']
        try:
            if file_name:
                oss_bucket.get_object_to_file(object_key, file_name, byte_range=byte_range, headers=headers)
            else:
                module.fail_json(msg="'file_name' must be specified when mode is get.")
            module.exit_json(changed=changed, key=object_key, object=get_object_info(oss_bucket.get_object_info(object_key)))
        except Exception as e:
            module.fail_json(msg="Unable to download object {0}, and got an error: {1}".format(object_key, e))

    elif mode == 'list':
        objects = []
        max_keys = 500
        try:
            while True:
                results = oss_bucket.list_objects(prefix=object_key, max_keys=max_keys)
                for obj in results:
                    objects.append(get_object_info(obj))

                if len(results) < max_keys:
                    break
            module.exit_json(changed=False, objects=objects)
        except Exception as e:
            module.fail_json(msg="Unable to retrieve all objects, and got an error: {0}".format(e))

    else:
        try:
            oss_bucket.delete_object(object_key)
            module.exit_json(changed=changed, key=object_key)
        except Exception as e:
            module.fail_json(msg="Unable to delete an object {0}, and got an error: {1}".format(object_key, e))


if __name__ == '__main__':
    main()

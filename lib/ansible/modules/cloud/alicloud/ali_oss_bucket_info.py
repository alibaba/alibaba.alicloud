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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_oss_bucket_info
version_added: "1.5.0"
short_description: Gather facts on buckets of Alibaba Cloud OSS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the OSS bucket itself.

options:
    bucket:
        description:
          - OSS bucket name.
        aliases: [ 'name' ]  
    bucket_prefix:
        description:
          - Prefix of OSS bucket name.         
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
#
# provisioning list oss buckets
#

# Basic provisioning example to create bucket
- name: List buckets detail example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    bucket: buctest1
    bucket_prefix: buctest1
  tasks:
    - name: List all buckets in the specified region
      ali_oss_bucket_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        bucket: '{{ bucket }}'
      register: all_buckets
    - debug: var=all_buckets

    - name: List all buckets in the specified region by name
      ali_oss_bucket_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        bucket: '{{ bucket }}'
        bucket_prefix: '{{ bucket_prefix }}'
      register: buckets_by_name
    - debug: var=buckets_by_name
'''

RETURN = '''
bucket_names:
    description: List all bucket's names in specified region.
    returned: when success
    type: list
    sample: ["xiaozhubucket", "testbucket"]
buckets:
    description: The list all buckets that has the prefix of 'bucket' value in the specified region
    returned: when list
    type: list
    sample: [
        {
            "id": "xiaozhubucket",
            "location": "oss-cn-beijing",
            "name": "xiaozhubucket",
            "permission": "private"
        },
        {
            "id": "testbucket",
            "location": "oss-cn-beijing",
            "name": "testbucket",
            "permission": "public-read-write"
        }
    ]
total:
    description: The number of all buckets available in region.
    returned: when success
    type: int
    sample: 2
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_oss import oss_bucket_argument_spec, oss_bucket_connect, oss_service_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError, OSSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(bucket):
    return {
        'id': bucket.id,
        'name': bucket.name,
        'permission': bucket.acl,
        'location': bucket.location
    }


def main():
    argument_spec = oss_bucket_argument_spec()
    argument_spec.update(
        dict(
            bucket=dict(aliases=["name"]),
            bucket_prefix=dict(type="str")
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    try:
        oss_service = oss_service_connect(module)
        keys = oss_service.list_buckets(prefix=module.params['bucket_prefix'], max_keys=200)

        buckets = []
        bucket_names = []
        for name in keys:
            module.params['bucket'] = name
            bucket = oss_bucket_connect(module)
            buckets.append(get_info(bucket))
            bucket_names.append(bucket.name)

        module.exit_json(changed=False, bucket_names=bucket_names, buckets=buckets, total=len(buckets))
    except Exception as e:
        module.fail_json(msg="Unable to describe buckets, and got an error: {0}.".format(e))


if __name__ == '__main__':
    main()

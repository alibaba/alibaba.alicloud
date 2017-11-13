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
module: alicloud_bucket
version_added: "2.4"
short_description: Create/Delete/Retrieve Bucket.
description:
    - This module allows the user to manage OSS buckets. Includes support for creating, deleting and retrieving buckets.
options:
  state:
    description:
      - Create or delete the OSS bucket. List all buckets that has the prefix of 'bucket' value.
    default: 'present'
    choices: [ 'present', 'absent', 'list']
  bucket:
    description:
      - Bucket name.
    required: true
    aliases: [ 'name' ]
  permission:
    description:
      - This option lets the user set the canned permissions on the bucket that are created.
    default: 'private'
    choices: [ 'private', 'public-read', 'public-read-write' ]
    aliases: [ 'acl' ]
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
# provisioning new oss bucket
#

# basic provisioning example to create bucket
- name: create oss bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    state: present
    bucket: bucketname
    permission: public-read-write
  tasks:
    - name: create oss bucket
      alicloud_bucket:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: '{{ state }}'
        bucket: '{{ bucket }}'
        permission: '{{ permission }}'
      register: result
    - debug: var=result

# basic provisioning example to delete bucket
- name: delete oss bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hangzhou
    state: absent
    bucket: bucketname
  tasks:
    - name: delete oss bucket
      alicloud_bucket:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: '{{ state }}'
        bucket: '{{ bucket }}'
      register: result
    - debug: var=result
'''

RETURN = '''
changed:
    description: current operation whether changed the resource
    returned: when success
    type: bool
    sample: true
bucket:
    description: the bucket's headers after create bucket or update its acl
    returned: on present
    type: dict
    sample: {
        "id": "xiaozhubucket",
        "location": "oss-cn-beijing",
        "name": "xiaozhubucket",
        "permission": "public-read"
    }
buckets:
    description: the list all buckets that has the prefix of 'bucket' value in the specified region
    returned: when list
    type: list
    sample: [
        {
            "id": "xiaozhubucket",
            "location": "oss-cn-beijing",
            "name": "xiaozhubucket",
            "permission": "public-read"
        },
        {
            "id": "xiaozhubucket-2",
            "location": "oss-cn-beijing",
            "name": "xiaozhubucket-2",
            "permission": "private"
        }
    ]
'''

# import module snippets
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_oss import oss_bucket_argument_spec, oss_bucket_connect, oss_service_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError, OSSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_bucket(bucket):
    return {'id': bucket.id, 'name': bucket.name, 'permission': bucket.acl, 'location': bucket.location}


def main():
    argument_spec = oss_bucket_argument_spec()
    argument_spec.update(
        dict(
            state=dict(required=True, choices=['present', 'absent', 'list']),
            permission=dict(default='private', choices=['private', 'public-read', 'public-read-write'], aliases=['acl']),
            bucket=dict(required=True, aliases=["name"]),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_bucket.")

    oss_bucket = oss_bucket_connect(module)
    state = module.params['state']
    permission = module.params['permission']

    if state == 'present':
        try:
            if oss_bucket.is_exist():
                result = oss_bucket.put_acl(permission=permission)
            else:
                result = oss_bucket.create(permission=permission)
            module.exit_json(changed=True, bucket=get_bucket(result))
        except Exception as e:
            module.fail_json(msg="Unable to put bucket or set acl for it, and got an error: {0}.".format(e))

    elif state == 'absent':
        try:
            oss_bucket.delete()
            module.exit_json(changed=True)
        except Exception as e:
            module.fail_json(msg="Unable to delete bucket, and got an error: {0}.".format(e))

    else:
        try:
            oss_service = oss_service_connect(module)
            keys = oss_service.list_buckets(prefix=module.params['bucket'], max_keys=200)

            buckets = []
            for name in keys:
                module.params['bucket'] = name
                buckets.append(get_bucket(oss_bucket_connect(module)))

            module.exit_json(changed=False, buckets=buckets)
        except Exception as e:
            module.fail_json(msg="Unable to list buckets, and got an error: {0}.".format(e))


if __name__ == '__main__':
    main()

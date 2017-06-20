#!/usr/bin/python
#
# Copyright 2017 Alibaba Group Holding Limited.
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

DOCUMENTATION = '''
---
module: oss
short_description: Create/Delete Bucket and Objects/Folder. Upload Files in OSS
description:
    - This module allows the user to manage OSS buckets and the objects within them. Includes support for
      creating and deleting both objects and buckets, retrieving object keys. This module has a dependency on footmark and ossutils.

common options:
  alicloud_access_key:
    description:
      - Aliyun Cloud access key. If not set then the value of the `ALICLOUD_ACCESS_KEY`, `ACS_ACCESS_KEY_ID`, 
        `ACS_ACCESS_KEY` or `ECS_ACCESS_KEY` environment variable is used.
    required: false
    default: null
    aliases: ['acs_access_key', 'ecs_access_key','access_key']
  alicloud_secret_key:
    description:
      - Aliyun Cloud secret key. If not set then the value of the `ALICLOUD_SECRET_KEY`, `ACS_SECRET_ACCESS_KEY`,
        `ACS_SECRET_KEY`, or `ECS_SECRET_KEY` environment variable is used.
    required: false
    default: null
    aliases: ['acs_secret_access_key', 'ecs_secret_key','secret_key']
  alicloud_region:
    description:
      - The Aliyun Cloud region to use. If not specified then the value of the `ALICLOUD_REGION`, `ACS_REGION`, 
        `ACS_DEFAULT_REGION` or `ECS_REGION` environment variable, if any, is used.
    required: false
    default: null
    aliases: ['acs_region', 'ecs_region', 'region']
  mode:
    description:
      - Switches the module behaviour between create (bucket), delete (bucket), put (upload), put_folder
        (create folder), list (list keys) and delobj (delete object).
    required: true
    choices: ['create', 'delete', 'put', 'put_folder', 'list', 'delobj']


function: create bucket
  description:
    - create bucket
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: [ 'bucket_name', 'name' ]
    permission:
      description:
        - This option lets the user set the canned permissions on the bucket that are created. The permissions that
          can be set are 'private', 'public-read', 'public-read-write'. Multiple permissions can be specified as a list.
      required: false
      default: private
      choices: [ 'private', 'public-read', 'public-read-write' ]

function: delete bucket
  description:
    - delete bucket
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: [ 'bucket_name', 'name' ]

function: put operation
  description:
    - upload a file
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: [ 'bucket_name', 'name' ]
    expiration:
      description:
        - Time limit (in seconds) for the URL generated and returned by OSS/Walrus when performing a mode=put or
          mode=geturl operation.
      required: false
      default: 600
       aliases: []
    headers:
      description:
        - Custom headers for PUT operation, as a dictionary of 'key=value' and 'key=value,key=value'.
      required: false
      default: null
    encrypt:
      description:
        - When set for PUT mode, asks for server-side encryption
      required: false
      default: no
    metadata:
      description:
        - Metadata for PUT operation, as a dictionary of 'key=value' and 'key=value,key=value'.
      required: false
      default: null
    overwrite:
      description:
        - Force overwrite either locally on the filesystem or remotely with the object/key. Used with PUT and GET
          operations. Boolean or one of [always, never, different], true is equal to 'always' and false is equal to
          'never'.
      required: false
      default: 'always'
    src:
      description:
        - The source file path when performing a PUT operation.
      required: true
      default: null
      aliases: []
    file_name:
      description:
        - Name to file after uploaded to bucket
      required: true
      default: null
      aliases: []

function: create folder in bucket
  description:
    - creates a folder in bucket
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: [ 'bucket_name', 'name' ]
    folder_name:
      description:
        - name of the folder to create
      required: true
      default: null

function: list bucket objects
  description:
    - list bucket object keys
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: [ 'bucket_name', 'name' ]
    marker:
      description:
        - Specifies the key to start with when using list mode. Object keys are returned in alphabetical order,
          starting with key after the marker in order
      required: false
      default: null
    max_keys:
      description:
        - Max number of results to return in list mode, set this if you want to retrieve fewer than the default 1000 keys.
      required: false
      default: 1000

function: delete bucket objects
  description:
    - delete objects in bucket
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: [ 'bucket_name', 'name' ]
    object_list:
      description:
        - Specify list of objects to delete from a bucket
      required: false
      default: null

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
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hangzhou
    mode: create
    bucket: bucketname
    permission: public-read-write    
  tasks:
    - name: create oss bucket
      oss:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        permission: '{{ permission }}'        
      register: result
    - debug: var=result

# basic provisioning example to delete bucket
- name: delete oss bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hangzhou
    mode: delete
    bucket: bucketname    
  tasks:
    - name: delete oss bucket
      oss:
        acs_access_key_id: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'        
      register: result
    - debug: var=result

# basic provisioning example to upload a file
- name: simple upload to bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hangzhou
    mode: put
    bucket: bucketname
    src: 'local_file.txt'
    file_name: 'remote_file.txt'
    headers:
      Content-Type: 'text/html'
      Content-Encoding: md5
    metadata:
      x-oss-meta-key: value
    expiration: 30    
  tasks:
    - name: simple upload to bucket
      oss:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        src: '{{ src }}'
        file_name: '{{ file_name }}'
        headers: '{{ headers }}'
        metadata: '{{ metadata }}'
        expiration: '{{ expiration }}'       
      register: result
    - debug: var=result

# basic provisioning example to create a folder in bucket
- name: create folder in a bucket
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hangzhou
    mode: put_folder
    bucket: bucketname
    folder_name: MeetingDocs
  tasks:
    - name: create bucket folder
      oss:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        folder_name: '{{ folder_name }}'
      register: folder_result
    - debug: var=folder_result

# basic provisioning example to list bucket objects
- name: list bucket objects
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hangzhou
    mode: list
    bucket: bucketname
    marker: xxxx
    max_keys: 150    
  tasks:
    - name: list bucket objects
      oss:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        marker: '{{ marker }}'
        max_keys: '{{ max_keys }}'
      register: list_result
    - debug: var=list_result

# basic provisioning example to delete bucket objects
- name: delete bucket objects
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hangzhou
    mode: delobj
    bucket: bucketname
    object_list:
      - objectname
      - objectname    
  tasks:
    - name: delete bucket objects
      oss:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        mode: '{{ mode }}'
        bucket: '{{ bucket }}'
        object_list: '{{ object_list }}'
      register: delete_objects_result
    - debug: var=delete_objects_result
'''

# import module snippets
import re
from ansible.module_utils.basic import *

try: 
    from ossutils.oss import *
except ImportError as ex:
    if 'footmark' in ex.message:
        msg = ex.message
    else:
        msg = "ossutils is required for the module"

    raise ImportError(msg)


def create_bucket(module, oss, permission):
    """
    Create OSS Bucket
    :param module: Ansible module object
    :param oss: Authenticated OSS connection object
    :param permission: This option lets the user set the canned permissions on the bucket that are created 
    :return: Details of newly created bucket
    """
    changed = False
    try:
        changed, result = oss.create_bucket(permission=permission)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except Exception as e:
        module.fail_json(msg='Unable to create bucket, error: {0}'.format(e))

    return changed, result


def delete_bucket(module, oss):
    """
    Delete OSS Bucket
    :param module: Ansible module object
    :param oss: Authenticated OSS connection object
    :return: Returns status of operation
    """
    changed = False
    try:
        changed, result = oss.delete_bucket()

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except Exception as e:
        module.fail_json(msg='Unable to delete bucket, error: {0}'.format(e))

    return changed, result


def simple_upload(module, oss, expiration=None, headers=None, encrypt=None, metadata=None, overwrite=None, src=None,
                  file_name=None):
    """
    Upload single file to Bucket
    :param module: Ansible module object
    :param oss: Authenticated OSS connection object
    :param expiration: Time limit (in seconds) for the URL generated and returned by OSS
    :param headers: Custom headers for PUT operation
    :param encrypt: When set for PUT mode, asks for server-side encryption
    :param metadata: Metadata for PUT operation, as a dictionary of 'key=value' and 'key=value,key=value'
    :param overwrite: Force overwrite either locally on the filesystem or remotely with the object/key
    :param src: The source file path when performing a PUT operation
    :param file_name: Name of after upload to bucket
    :return: Details of uploaded file in bucket
    """
    changed = False
    try:
        if file_name is None:
            module.fail_json(msg='file_name is required for file uploading')  

        if src is None:
            module.fail_json(msg='src is required for file uploading')

        if expiration < 0:
            module.fail_json(msg='invalid expiration value')       

        changed, result = oss.simple_upload(expiration=expiration, headers=headers, encrypt=encrypt, metadata=metadata,
                                            overwrite=overwrite, src=src, file_name=file_name)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except Exception as e:
        module.fail_json(msg='Unable to upload file, error: {0}'.format(e))

    return changed, result


def create_bucket_folder(module, bucket, folder_name):
    """
    Create folder in a bucket

    :param module: Ansible module object
    :param bucket: Authenticated OSS Bucket connection object
    :param folder_name: folder_name to be created
    :return: returns changed status and custom message
    """

    try:
        # verifying and adding '/' in the provided folder name
        if not folder_name.endswith("/"):                        
                folder_name += "/"

        # check whether special characters in folder name
        if not re.match("^[A-Za-z0-9]*$", folder_name[:-1]):
            module.fail_json(msg='invalid folder name')         

        if len(folder_name[:-1]) > 254:
            module.fail_json(msg='folder name must have less than 254 characters')         

        # verifying if folder is already present
        object_exists, error_if_any = bucket.object_exists(folder_name)
        if object_exists:
            module.exit_json(changed=False, msg="Folder already exists")
        elif error_if_any:
            module.fail_json(changed=False, msg=error_if_any)

        # creating folder
        changed, results = bucket.create_folder(folder_name)

        if 'error' in str(results).lower():
            module.fail_json(changed=changed, msg=results)

        return changed, results

    except Exception as e:
        module.fail_json(msg='Unable to create bucket folder, error: {0}'.format(e))


def list_bucket_objects(module, bucket, max_keys, marker=None):
    """
    List objects of a bucket
    :param module: Ansible module object
    :param bucket: Authenticated OSS Bucket connection object
    :param marker: marker to get matching objects
    :param max_keys: no of objects to retrieve
    :return: objects if any and custom message
    """

    try:
        # validating max_keys between 1-1000
        if max_keys > 1000 or max_keys < 1:
            module.fail_json(msg="max_keys allowed in the range of 1-1000")

        # listing bucket objects
        keys, results = bucket.list_bucket_objects(marker=marker, max_keys=max_keys)

        if 'error' in str(results).lower():
            module.fail_json(changed=False, msg=results)

        return keys, results

    except Exception as e:
        module.fail_json(msg='Unable to list bucket objects, error: {0}'.format(e))


def delete_bucket_objects(module, bucket, objects_to_delete=None):
    """
    Delete bucket objects
    :param module: Ansible module object
    :param bucket: Authenticated OSS Bucket connection object
    :param objects_to_delete: specific objects to delete. If none provided, deletes all objects
    :return: changed status, custom message and deleted objects
    """

    try:
        result = []
        changed = False

        # verify whether provided objects exist and if no objects provided then get all objects to delete
        available_objects_to_delete, absent_objects = look_up_objects(module, bucket, objects_to_delete)

        if available_objects_to_delete:
            changed, result = bucket.delete_bucket_objects(available_objects_to_delete)
        else:
            module.exit_json(changed=changed, msg="No valid objects to delete")

        return changed, available_objects_to_delete, absent_objects, result

    except Exception as e:
        module.fail_json(msg='Unable to delete bucket objects, error: {0}'.format(e))


def look_up_objects(module, bucket, objects):
    """
    Get available and absent objects from the provided list or get all objects of a bucket
    :param module: Ansible module object
    :param bucket: Authenticated OSS Bucket connection object
    :param objects: objects to verify for existence
    :return: returns found objects
    """

    found_objects = []
    absent_objects = []

    # if objects provided verify if it exists
    if objects is not None:

        for bucket_object in objects:
            object_exists, error_if_any = bucket.object_exists(bucket_object)
            if object_exists:
                found_objects.append(bucket_object)
            elif error_if_any:
                module.fail_json(msg=error_if_any)
            else:
                absent_objects.append(bucket_object)

    # if no objects provided then get all objects of the bucket
    else:
        keys, result = bucket.list_bucket_objects()
        if 'error' in str(result).lower():
            module.fail_json(msg=result)

        found_objects.extend(keys)

    if len(found_objects) == 0:
        found_objects = None

    if len(absent_objects) == 0:
        absent_objects = None

    return found_objects, absent_objects


def main():
    argument_spec = oss_bucket_argument_spec()
    argument_spec.update(dict(
        mode=dict(required=True, choices=['create', 'delete', 'put', 'put_folder', 'list', 'delobj']),
        permission=dict(default='private', choices=['private', 'public-read', 'public-read-write']),
        expiration=dict(type='int', default=600),
        headers=dict(type='dict'),
        encrypt=dict(),
        metadata=dict(type='dict'),
        overwrite=dict(),
        src=dict(),
        file_name=dict(),
        folder_name=dict(type='str'),
        object_list=dict(type='list'),
        marker=dict(type='str'),
        max_keys=dict(default='1000', type='int'),
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    oss_bucket = oss_bucket_connect(module)
    mode = module.params['mode']
    folder_name = module.params['folder_name']
    objects_list = module.params['object_list']
    marker = module.params['marker']
    max_keys = module.params['max_keys']

    if mode == 'create':
        permission = module.params['permission']
        (changed, result) = create_bucket(module=module, oss=oss_bucket, permission=permission)
        module.exit_json(changed=changed, result=result)

    elif mode == 'delete':
        (changed, result) = delete_bucket(module=module, oss=oss_bucket)
        module.exit_json(changed=changed, result=result)

    elif mode == 'put':
        expiration = module.params['expiration']
        headers = module.params['headers']
        encrypt = module.params['encrypt']
        metadata = module.params['metadata']
        overwrite = module.params['overwrite']
        src = module.params['src']
        file_name = module.params['file_name']

        (changed, result) = simple_upload(module=module, oss=oss_bucket, expiration=expiration, headers=headers,
                                          encrypt=encrypt, metadata=metadata, overwrite=overwrite, src=src,
                                          file_name=file_name)

        module.exit_json(changed=changed, result=result)

    elif mode == 'put_folder':
        if folder_name is None:
            module.fail_json(msg='folder_name is required')

        changed, results = create_bucket_folder(module, oss_bucket, folder_name)
        module.exit_json(changed=changed, msg=results)

    elif mode == 'list':
        keys, results = list_bucket_objects(module, oss_bucket, marker=marker, max_keys=max_keys)
        module.exit_json(changed=False, keys=keys, msg=results)

    elif mode == 'delobj':
        changed, deleted_keys, absent_keys, results = delete_bucket_objects(module, oss_bucket, objects_list)
        module.exit_json(changed=changed, deleted_keys=deleted_keys, absent_keys=absent_keys, msg=results)


main()

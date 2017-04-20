#!/usr/bin/python
# This file is part of Ansible

DOCUMENTATION = '''
---
module: oss
short_description: manage objects in OSS.
description:
    - This module allows the user to manage OSS buckets and the objects within them. Includes support for creating and deleting both objects and buckets, retrieving objects as files or strings and generating download links. This module has a dependency on python-footmark.
common options:
  acs_access_key:
    description: The access key.
    required: false
    default: null
    aliases: []
  acs_secret_access_key:
    description: The access secret key.
    required: false
    default: null
    aliases: []
  mode:
    description:
      - Switches the module behaviour between put (upload), get (download), geturl (return download url), getstr (download object as string), list (list keys), create (bucket), delete (bucket), and delobj (delete object).
    required: true
    choices: ['get', 'put', 'delete', 'create', 'geturl', 'getstr', 'delobj', 'list']

function: put operation
  description: put operation
  options:
    expiration:
      description:
        - Time limit (in seconds) for the URL generated and returned by OSS/Walrus when performing a mode=put or mode=geturl operation.
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
        - Force overwrite either locally on the filesystem or remotely with the object/key. Used with PUT and GET operations. Boolean or one of [always, never, different], true is equal to 'always' and false is equal to 'never'.
      required: false
      default: 'always'
    src:
      description:
        - The source file path when performing a PUT operation.
      required: false
      default: null
      aliases: []

function: get operation
  description: get operation
  options:
    dest:
      description:
        - The destination file path when downloading an object/key with a GET operation.
      required: false
      aliases: []
    overwrite:
      like put operation

function: geturl operation
  description: geturl operation
  options:
    expiration:
      like put operation

function: list operation
  description: list operation
  options:
    expiration:
      like put operation
    marker:
    description:
      - Specifies the key to start with when using list mode. Object keys are returned in alphabetical order, starting with key after the marker in order.
    required: false
    default: null
  max_keys:
    description:
      - Max number of results to return in list mode, set this if you want to retrieve fewer than the default 1000 keys.
    required: false
    default: 1000

function: create bucket
  description: create bucket
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: []
    permission:
      description:
        - This option lets the user set the canned permissions on the bucket that are created. The permissions that can be set are 'private', 'public-read', 'public-read-write'. Multiple permissions can be specified as a list.
      required: false
      default: private
    region:
      description:
       - "ACS region to create the bucket in. If not set then the value of the ACS_REGION and ECS_REGION environment variables are checked. If none of those are set the region defaults to the OSS Location: oss-cn-hangzhou"
      required: false
      default: oss-cn-hangzhou
      choices: ['oss-cn-hangzhou', 'oss-cn-qingdao', 'oss-cn-beijing', 'oss-cn-hongkong', 'oss-cn-shenzhen', 'oss-cn-shanghai', 'oss-us-west-1', 'oss-ap-southeast-1']

function: delete bucket
  description: delete bucket
  options:
    bucket:
      description:
        - Bucket name.
      required: true
      default: null
      aliases: []

requirements: [ "footmark" ]
author:
    - "xiaozhu"
'''

EXAMPLES = '''
# Simple PUT operation
- oss: bucket=mybucket object=/my/desired/key.txt src=/usr/local/myfile.txt mode=put
# Simple GET operation
- oss: bucket=mybucket object=/my/desired/key.txt dest=/usr/local/myfile.txt mode=get
# PUT/upload with metadata
- oss: bucket=mybucket object=/my/desired/key.txt src=/usr/local/myfile.txt mode=put metadata='Content-Encoding=gzip,Cache-Control=no-cache'
# PUT/upload with custom headers
- oss: bucket=mybucket object=/my/desired/key.txt src=/usr/local/myfile.txt mode=put headers=x-amz-grant-full-control=emailAddress=owner@example.com
# List keys simple
- oss: bucket=mybucket mode=list
# List keys all options
- oss: bucket=mybucket mode=list prefix=/my/desired/ marker=/my/desired/0023.txt max_keys=472
# Create an empty bucket
- oss: bucket=mybucket mode=create permission=public-read
# Create a bucket with key as directory, in the EU region
- oss: bucket=mybucket object=/my/directory/path mode=create region=eu-west-1
# Delete a bucket and all contents
- oss: bucket=mybucket mode=delete
# Delete an object from a bucket
- oss: bucket=mybucket object=/my/desired/key.txt mode=delobj
'''
#!/usr/bin/python
# This file is part of Ansible
DOCUMENTATION = '''
---
module: ros
short_description: Create or delete an Alicloud ROS stack
description:
     - Launches an ACS CloudFormation stack and waits for it complete.
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
  state:
    description:
      - If state is "present", stack will be created.  If state is "present" and if stack exists and template has changed, it will be updated.
        If state is "absent", stack will be removed.
    required: true
    default: null

function: create instance
  description: create an instance in ecs
  options:
      stack_name:
        description:
          - name of the ros stack
        required: true
      disable_rollback:
        description:
          - If a stacks fails to form, rollback will remove the stack
        required: false
        default: "false"
        choices: [ "true", "false" ]
      template_parameters:
        description:
          - a list of hashes of all the template variables for the stack
        required: false
        default: {}
      template:
        description:
          - The local path of the ros template. This parameter is mutually exclusive with 'template_url'. Either one of them is required if "state" parameter is "present"
            Must give full path to the file, relative to the working directory. If using roles this may look like "roles/ros/files/-example.json"
        required: false
        default: null
      region:
        description:
          - The ACS region to use. If not specified then the value of the ACS_REGION or ECS_REGION environment variable, if any, is used.
        required: true
        aliases: ['acs_region', 'ecs_region']
      template_url:
        description:
          - Location of file containing the template body. The URL must point to a template (max size 307,200 bytes) located in an S3 bucket in the same region as the stack. This parameter is mutually exclusive with 'template'. Either one of them is required if "state" parameter is "present"
        required: false
      template_format:
        description:
        - For local templates, allows specification of json or yaml format
        default: json
        choices: [ json, yaml ]
        required: false
function: delete instance
  description: delete an instance in ecs
  options:
      stack_name:
        description:
          - name of the ros stack
        required: true
      stack_id:
        description:
          - id of the ros stack
        required: true
      region:
        description:
          - The ACS region to use. If not specified then the value of the ACS_REGION or ECS_REGION environment variable, if any, is used.
        required: true
        aliases: ['acs_region', 'ecs_region']
author: "Xiaozhu"
'''

EXAMPLES = '''
# Basic task example
- name: launch ansible ros example
  ros:
    stack_name: "ansible-ros"
    state: "present"
    region: "cn-shenzhen-a"
    disable_rollback: true
    template: "files/ros-example.json"
    template_parameters:
      KeyName: "jmartin"
      DiskType: "cloud_ssd"
      InstanceType: "ecs.s2.small"
      ClusterSize: 3
# Basic role example
- name: launch ansible ros example
  ros:
    stack_name: "ansible-ros"
    state: "present"
    region: "cn-shenzhen-a"
    disable_rollback: true
    template: "roles/ros/files/ros-example.json"
    template_parameters:
      KeyName: "jmartin"
      DiskType: "cloud_ssd"
      InstanceType: "ecs.s2.small"
      ClusterSize: 3
# Removal example
- name: tear down old deployment
  ros:
    stack_name: "ansible-ros-old"
    state: "absent"
# Use a template from a URL
- name: launch ansible ros example
  ros:
    stack_name="ansible-ros" state=present
    region=us-east-1 disable_rollback=true
    template_url=https://s3.amazonacs.com/my-bucket/ros.template
  args:
    template_parameters:
      KeyName: jmartin
      DiskType: cloud_ssd
      InstanceType: ecs.s2.small
      ClusterSize: 3
'''
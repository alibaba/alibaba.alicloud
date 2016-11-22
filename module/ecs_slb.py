#!/usr/bin/python
# This file is part of Ansible.

DOCUMENTATION = """
---
module: ecs_elb
short_description: De-registers or registers instances from ECS SLBs
description:
  - This module de-registers or registers an ACS ECS instance from the SLBs
    that it belongs to.
  - Returns fact "ecs_elbs" which is a list of elbs attached to the instance
    if state=absent is passed as an argument.
  - Will be marked changed when called only if there are SLBs found to operate on.
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
      - register or deregister the instance
    choices: ["present", "absent"]
    required: true

function register the instance
    state: present
    options:
      instance_id:
        description:
          - ECS Instance ID
        required: true
      ecs_elbs:
        description:
          - List of SLB names, required for registration.
        required: false
        default: None
      enable_availability_zone:
        description:
          - Whether to enable the availability zone of the instance on the target SLB if the availability zone has not already
            been enabled. If set to no, the task will fail if the availability zone is not enabled on the SLB.
        required: false
        default: yes
        choices: [ "yes", "no" ]
      validate_certs:
        description:
          - When set to "no", SSL certificates will not be validated.
        required: false
        default: "yes"
        choices: ["yes", "no"]
        aliases: []

function register the instance
    state: absent
    options:
      instance_id:
        like state=present
      ecs_elbs:
        like state=present
"""

EXAMPLES = """
# basic pre_task and post_task example
pre_tasks:
  - name: Gathering ecs facts
    action: ecs_facts
  - name: Instance De-register
    local_action:
      module: ecs_elb
      instance_id: "{{ ansible_ecs_instance_id }}"
      state: absent
roles:
  - myrole
post_tasks:
  - name: Instance Register
    local_action:
      module: ecs_elb
      instance_id: "{{ ansible_ecs_instance_id }}"
      ecs_elbs: "{{ item }}"
      state: present
    with_items: ecs_elbs
"""
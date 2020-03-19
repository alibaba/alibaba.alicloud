Role Name
=========

filter resources and add tags for them.
- ECS
- VPC
- Vswitch
- Security_Group

The version of python is 3.6

Requirements
------------

Before you use this role, you must install below, like this 'pip install ansible-alicloud'':
- ansible-alicloud

Role Variables
--------------

state: present
alicloud_region: "cn-hangzhou"

#### default tags
tags: {env: prod, source: ansible, usage: poc}

#### ecs instance filter parameters and tags
instance_name: ''
instance_filters: {}
instance_tags: {}

#### security group filter parameters and tags
security_group_name: ''
security_group_filters: {}
security_group_tags: {}

#### vpc filter parameters and tags
vpc_name: ''
vpc_filters: {}
vpc_tags: {}

#### vswitch filter parameters and tags
vswitch_name: ""
vswitch_filters: {}
vswitch_tags: {}

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - tags:
           instance_name: 'Ansible_Instance'
           instance_tags: {For: Ansible}
           state: absent


License
-------

GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Author Information
------------------
- "He Guimin (@xiaozhu36)"
- "Li Xue (@lixue323)"
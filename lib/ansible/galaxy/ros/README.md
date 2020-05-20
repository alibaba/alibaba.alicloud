Role Name
=========

- Specify ECS InstanceId to Create a of ECS Instance with the Same Configuration by Ros Stack
- The version of python is 3.6

Requirements
------------

Before you use this role, you must install below, like this 'pip install ansible-alicloud':
- ansible-alicloud

Role Variables
--------------
alicloud_region:
- description: Alibaba Cloud resource region domain
- type: string
- sample: cn-beijing

state:
- description: The management status of the ali_ros_stack corresponding resource, There are two states present/absent, For creation and deletion.
- type: string
- sample: present

stack_name:
- description: Ros stack resources name.
- type: string
- sample: copy_ecs_by_ros

timeout_in_minutes:
- description: Ros stack resources create timeout time, default value is 60 minutes.
- type: int
- sample: 60

create_instance_name:
- description: Instance names created with Ros replication.
- type: string
- sample: Instance_From_Ros

password:
- description: Instance password created with Ros replication.
- type: string
- sample: Test12345

template:
- description: Ros template file copy to path
- type: string
- sample: /tmp/ros_copy_instance_template.json

instance_id:
- description: Get copied instances by instance_id, If you do not use this mode to filter, you can set empty.
- type: string
- sample: i-2ze50dakjhda

instance_name_prefix:
- description: Get copied instances by instance name regex, If you do not use this mode to filter, you can set empty.
- type: string
- sample: get_ecs

instance_tags:
- description: Get copied instances by instance tags, If you do not use this mode to filter, you can set empty.
- type: dict
- sample: {Test: add}

instance_filters:
- description: Get copied instances by instance filters. About parameter details , See :https://www.alibabacloud.com/help/doc-detail/25506.htm, If you do not use this mode to filter, you can set empty.
- type: dict
- sample: {vpc_id: vpc-2zepuqws}

Example Playbook
----------------

    - hosts: servers
      roles:
         - role: ros
           instance_id: i-2ze50dakjhda
           stack_name: copy_instance_by_ros
           
License
-------

GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Author Information
------------------
- "Steven"
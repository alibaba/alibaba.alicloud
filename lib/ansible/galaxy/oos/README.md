Role Name
=========

- Cross Region copy and run ECS instance by InstanceIds
- The version of python is 3.6

Requirements
------------

Before you use this role, you must install below, like this 'pip install ansible-alicloud':
- ansible-alicloud

Role Variables
--------------
alicloud_region:
- description: Alibaba Cloud resource region domain.
- type: string
- sample: cn-beijing

state:
- description: The management status of the ali_ros_stack corresponding resource, There are two states present/absent, For creation and deletion.
- type: string
- sample: present

template_name:
- description: Oos templates name.
- type: string
- sample: clone_instances_across_region

content:
- description: Oos template file copy to path.
- type: string
- sample: /tmp/roles/oos/files/clone_instances_across_region_by_oos.json

instance_id:
- description: Get copied instances by instance_id, If you do not use this mode to filter, you can set empty.
- type: string
- sample: i-2123test

region_id:
- description: The Source Region Id.
- type: string
- sample: cn-hangzhou

target_region_id:
- description: The Target Region Id.
- type: string
- sample: cn-beijing

target_zone_id:
- description: The Target Zone Id.
- type: string
- sample: cn-beijing-h

target_instance_type:
- description: The instance type for the ECS instances.
- type: string
- sample: ecs.g5.large

target_security_groupId:
- description: The security group ID for the ECS instances.
- type: string
- sample: sg-xxxxxxxxxxxxxxxxxxxx

target_vSwitchId:
- description: The virtual switch ID for the ECS instances
- type: string
- sample: vsw-xxxxxxxxxxxxxxxxxxxx

Example Playbook
----------------

    - hosts: servers
      roles:
         - role: oos
           instance_id: [i-bp1d3xxxxxxxx]
           target_security_groupId: sg-2ze55xxxxxxxx
           target_vSwitchId: vsw-2zekbixxxxxxxx
           target_instance_type: ecs.g6.large
           region_id: cn-hangzhou
           target_region_id: cn-beijing
           target_zone_id: cn-beijing-h
           
License
-------

GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Author Information
------------------
- "Kang"

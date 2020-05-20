Role Name
=========

- Specify ECS InstanceId to Create a Group of ECS Instances with the Same Configuration by Ros Stack
- The version of python is 3.6

Requirements
------------

Before you use this role, you must install below, like this 'pip install ansible-alicloud'':
- ansible-alicloud

Role Variables
--------------
alicloud_region: cn-beijing

#### ecs instance filter parameters
instance_name: Instance_From_Ros
instance_tags: {For: Ros, Created: Ansible, From: role/ros}
image_id: "ubuntu_18_04_x64_20G_alibase_20200426.vhd"
instance_type: ecs.sn2ne.large
instance_description: "Create a new ECS instance resource via role ros."
host_name: "my-instance-from-ansible"
password: Test12345

allocate_public_ip: True
internet_charge_type: "PayByTraffic"
max_bandwidth_in: 200
max_bandwidth_out: 50

system_disk_category: "cloud_ssd"
system_disk_size: 50
number_of_instances: 1

#### security group filter parameters
security_group_name: 'Security_Group_From_Ansible_Ros'
security_group_tags: {For: Ros, Created: Ansible, From: example/ros}

group_description: "Create a new security group resource via Ansible example ros."
group_inboundRules:
  - ip_protocol: tcp
    port_range: 22/22
    source_cidr_ip: 0.0.0.0/0
    priority: 1

  - ip_protocol: tcp
    port_range: 80/80
    source_cidr_ip: 0.0.0.0/0
    priority: 1

group_outboundRules:
  - ip_protocol: tcp
    port_range: 80/80
    dest_cidr_ip: 192.168.0.54/32
    priority: 1

#### vpc filter parameters
vpc_name: 'Vpc_From_Ansible_Ros'
vpc_tags: {For: Ros, Created: Ansible, From: example/ros}
vpc_cidr: "172.16.0.0/12"
vpc_description: "Create a new VPC resource via Ansible example ros."

#### vswitch parameters
availability_zone: "cn-beijing-f"
vswitch_cidr: "172.16.1.0/24"
vswitch_description: "Create a new VSwitch resource via Ansible example ros."
vswitch_name: 'Vswitch_From_Ansible_Ros'


Example Playbook
----------------

    - hosts: servers
      roles:
         - ros
           stack_name: 'copy_instance_by_ros'
           
License
-------

GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Author Information
------------------
- "Steven"
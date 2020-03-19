Role Name
=========

- Search market product and use image to create ecs
- The version of python is 3.6

Requirements
------------

Before you use this role, you must install below, like this 'pip install ansible-alicloud'':
- ansible-alicloud

Role Variables
--------------
alicloud_region: cn-beijing

#### market product info
product_keyword: Wordpress
product_supplier_name_keyword: ''
product_suggested_price: 0
product_name_prefix: ''
product_type: ""
product_sort: ''
product_category_id: ''
product_ids: ''
product_supplier_id: ''

#### ecs instance filter parameters
instance_name: ['Instance_From_Ansible_Market', 'a-Instance_From_Ansible_Market']
instance_tags: {For: Market, Created: Ansible, From: example/market}
image_id: "ubuntu_18_04_64_20G_alibase_20190624.vhd"
instance_type: ecs.g5.large
instance_description: "Create a new ECS instance resource via Ansible example market."
password: YourPassword123

allocate_public_ip: True
internet_charge_type: "PayByTraffic"
max_bandwidth_in: 200
max_bandwidth_out: 50

system_disk_category: "cloud_ssd"
system_disk_size: 50
number_of_instances: 1

#### security group filter parameters
security_group_name: 'Security_Group_From_Ansible_Market'
security_group_tags: {For: Market, Created: Ansible, From: example/market}

group_description: "Create a new security group resource via Ansible example market."
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
vpc_name: 'Vpc_From_Ansible_Market'
vpc_tags: {For: Market, Created: Ansible, From: example/market}
vpc_cidr: "172.16.0.0/12"
vpc_description: "Create a new VPC resource via Ansible example market."

#### vswitch parameters
availability_zones: ["cn-beijing-e", "cn-beijing-f"]
vswitch_cidr: ["172.16.1.0/24", "172.22.0.0/16"]
vswitch_description: "Create a new VSwitch resource via Ansible example market."
vswitch_name: 'Vswitch_From_Ansible_Market'


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - market
           product_keyword: 'Wordpress'
           password: MyPassword
           number_of_instances: 2
           
License
-------

GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Author Information
------------------
- "He Guimin (@xiaozhu36)"
- "Li Xue (@lixue323)"
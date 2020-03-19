Role Name
=========

- You can use this role to deploy petstore on alicloud ecs, it supports set variable zone, and deploy on multiple instances.
- The version of python is 3.6

Requirements
------------
Before you use this role, you must install below, like this 'pip install ansible-alicloud'':
- ansible-alicloud
- ansible_alicloud_module_utils


Role Variables
--------------

#### ecs instance filter parameters

exist: False
alicloud_path: ./
instance_name: ['Instance_From_Ansible_Petstore', 'a-Instance_From_Ansible_Petstore']
instance_tags: {For: PetStore, Created: Ansible, From: example/deploy}
image_id: "ubuntu_18_04_64_20G_alibase_20190624.vhd"
instance_type: ecs.sn2ne.large
instance_description: "Create a new ECS instance resource via Ansible example deploy-ecs."
host_name: "my-instance-from-ansible"
password: Test12345

allocate_public_ip: True
internet_charge_type: "PayByTraffic"
max_bandwidth_in: 200
max_bandwidth_out: 50

system_disk_category: "cloud_ssd"
system_disk_size: 50
number_of_instances: 2

#### security group filter parameters
security_group_name: 'Security_Group_From_Ansible'
security_group_tags: {For: PetStore, Created: Ansible, From: example/deploy}

group_description: "Create a new security group resource via Ansible example deploy-ecs."
group_inboundRules:
  - ip_protocol: tcp
    port_range: 22/22
    source_cidr_ip: 0.0.0.0/0
    priority: 1

  - ip_protocol: tcp
    port_range: 80/80
    source_cidr_ip: 0.0.0.0/0
    priority: 1

  - ip_protocol: tcp
    port_range: 8081/8081
    source_cidr_ip: 0.0.0.0/0
    priority: 1

group_outboundRules:
  - ip_protocol: tcp
    port_range: 80/80
    dest_cidr_ip: 192.168.0.54/32
    priority: 1

#### vpc filter parameters
vpc_name: 'Vpc_From_Ansible'
vpc_tags: {For: PetStore, Created: Ansible, From: example/deploy}
vpc_cidr: "172.16.0.0/12"
vpc_description: "Create a new VPC resource via Ansible example-deploy-ecs."

#### vswitch parameters
availability_zones: ["cn-beijing-e", "cn-beijing-f"]
vswitch_cidrs: ["172.16.1.0/24", "172.22.0.0/16"]
vswitch_description: "Create a new VSwitch resource via Ansible example-deploy-ecs."
vswitch_name: 'Vswitch_From_Ansible'


Example Playbook
----------------
- Before you use this role, Execute the following command to download the latest version of alicloud dynamic inventory file
        wget https://raw.githubusercontent.com/alibaba/ansible-provider/master/contrib/inventory/alicloud.py
        chmod +x alicloud.py
        wget https://raw.githubusercontent.com/alibaba/ansible-provider/master/contrib/inventory/alicloud.ini

- Configure your authentication:
        alicloud.ini
        alicloud_access_key = Abcd1234 
        alicloud_secret_key = Abcd2345

        or 
        
        environment variable
        export ALICLOUD_ACCESS_KEY = Abcd1234
        export ALICLOUD_SECRET_KEY = Abcd2345

- Configure filter parameters in the INI file to filter out the target host
   
#### Finally use role to deploy:

    - hosts: servers
      roles:
         - deploy
           exist: False
           alicloud_path: /tmp/alicloud.py
           number_of_instances: 4

License
-------

GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Author Information
------------------
- "He Guimin (@xiaozhu36)"
- "Li Xue (@lixue323)"
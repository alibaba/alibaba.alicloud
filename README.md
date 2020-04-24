# Ansible Collection - alibaba.alicloud

## Installation and Usage
#### Installing the Collection from Ansible Galaxy
Before using the alicloud collection, you need to install the collection with the ansible-galaxy CLI:
```
ansible-galaxy collection install alibaba.alicloud
```
#### Installing dependency footmark
```
pip install footmark
```

#### Usage
```
collections:
- name: alibaba.alicloud
```

## Include modules
- `ali_instance`: Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group
- `ali_disk`: Create, Attach, Detach or Delete a disk in ECS
- `ali_dns_domian`: Create, Delete and Update DNS domain
- `ali_dns_group`: Create, Delete and Update DNS group
- `ali_ecs_tag`: Add tags for alicloud resource
- `ali_eip`: Create eip address and bind it to a specified device
- `ali_image`: Create or delete user-defined image
- `ali_market_product_info`: Gather info on Market product of alicloud
- `ali_oos_execution`: Create, Delete, Notify, Cancel OOS Execution
- `ali_oos_template`: Create, Delete, Update OOS template
- `ali_oss_bucket`: Create, Delete, Retrieve Bucket
- `ali_oss_object`: Uploading and Downloading objects, Retrieving object keys
- `ali_ram_access_key`: Create, Delete Ram Access Key and Update status
- `ali_ram_group`: Create, Delete, Update Ram group
- `ali_ram_login_profile`: Create, Delete, Update Ram login profile
- `ali_ram_policy`: Create, Delete, Attach and Detach Ram policy
- `ali_ram_role`: Create, Delete, Update Ram Role
- `ali_ram_user`: Create, Delete, Update Ram User
- `ali_rds_account`: Create, Delete, Modyfy, Reset rds account and Grant, Revoke privilege
- `ali_rds_backup`: Create, Delete rds backup
- `ali_rds_database`: Create, Delete or Copy an rds database
- `ali_rds_instance`: Create, Restart or Delete an RDS Instance
- `ali_ros_stack`: Create, Delete and Modify for ROS Stack
- `ali_security_group`: Create or Delete a Security Group
- `ali_vpc.py`: Create or Delete a Vpc
- `ali_vswitch`: Create or Delete a VSwitch
- `ali_route_entry`: Create or Delete a route entry
- `ali_slb_lb`: Create or Delete a Load balancer
- `ali_slb_listener`: Create or Delete a listener for one Load balancer
- `ali_slb_server`: Add or Remove backend server to/from Load balancer
- `ali_slb_vsg`: Create and delete a VServer group
- `ali_ess_group`: Create or Delete a scaling group
- `ali_ess_configuration`: Create or Delete a scaling configuration
- `ali_ess_instance`: Add or Remove ECS instnaces in a specified scaling group
- `ali_ess_task`: Create or Delete a scheduled task for scaling activity
- `ali_ess_rule`: Create or Delete a scaling rule
- `ali_eni`: Create or Delete a network interface


## Inventory plugin
#### Usage
config file
```
alicloud.yaml

plugin: alibaba.alicloud.alicloud_ecs
```
Execute command line
```
ansible-inventory -i alicloud.yml --graph
```

## DOC
Ansible Document: https://docs.ansible.com/ansible/latest/

Ansible Alicloud: [Docs Details](http://47.88.222.42:8080/ansible-alicloud/latest/modules/list_of_cloud_modules.html)
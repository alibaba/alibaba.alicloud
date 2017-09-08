# Ansible ECS Module

Ansible Alicloud Module is a new ansible module, and you can manage Alicloud ECS and other services more flexibly and conveniently via it. Next to introduce simply this module.
## lib/ansible/modules/cloud/alicloud
There are several files in the module directory, and these files describe some function that can operate alicloud products.

- `alicloud_instance.py`: Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group
- `alicloud_disk.py`: Create, Attach, Detach or Delete a disk in ECS
- `alicloud_security_group.py`: Create or Delete a Security Group
- `alicloud_vpc.py`: Create or Delete a Vpc.
- `alicloud_vswitch.py`: Create or Delete a VSwitch.
- `alicloud_route_entry.py`: Create or Delete a route entry.
- `alicloud_slb_lb.py`: Create or Delete a Load balancer.
- `alicloud_slb_listener.py`: Create or Delete a listener for one Load balancer.
- `alicloud_slb_server.py`: Add or Remove backend server to/from Load balancer.

- `alicloud_bucket.py`: Create or Delete an OSS bucket.
- `alicloud_bucket_object.py`: Upload or Download an object to/from an OSS bucket.

## lib/ansible/module_utils
In the module utils directory, the file alicloud_ecs.py identifies and gains playbook params, and provides this params to modules/*.py. In addition, this file implements connection between ansible and Alicloud API via footmark.

## examples
There are some playbooks to create some alicloud resource or build infrastructure architecture.

### Install
There are two ways to install alicloud provider. However, before installing it. you should ensure `Ansible` has existed in your server.
If not, please install it using the following command:

    sudo pip install ansible

* First one

    Ansible provider has been released, and you can install it easily using the following command:

      sudo pip install ansible_alicloud

* Second one

    Ansible provider's modules support to install independently. That means you can download one or more modules from lib/ansible/modules/cloud/alicloud and then run them independently.
    However, before running them, you should ensure `ansible_alicloud_module_utils` has existed in your server. If not, please install it using the following command:

      sudo pip install ansible_alicloud_module_utils

### Execute playbook

* Input your alicloud access key in the playbook or set environment variable:`ALICLOUD_ACCESS_KEY` and `ALICLOUD_SECRET_KEY`).
* Input others resource params in the playbook.
* execute ansible-playbook command as follows:

	  $ ansible-playbook xxx.yml
	   

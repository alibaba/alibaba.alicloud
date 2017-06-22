# Ansible ECS Module

[![Build Status](https://travis-ci.org/Click2Cloud/ansible-provider.svg?branch=master)](https://travis-ci.org/Click2Cloud/ansible-provider)

Ansible Alicloud Module is a new ansible module, and you can manage Alicloud ECS and other services more flexibly and conveniently via it. Next to introduce simply this module.
## lib/ansible/modules/cloud/alicloud
There are several files in the module directory, and these files describe some function that can operate alicloud products.

- `alicloud_instance.py`: Create, Start, Stop, Query, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group
- `alicloud_disk.py`: Create, Attach, Detach or Delete a disk in ECS
- `alicloud_security_group.py`: Create, Query or Delete Security Group
- `alicloud_vpc.py`: Create Delete and Query Vpc.
- `alicloud_vswitch.py`: Create Delete and Query VSwitch.

## lib/ansible/module_utils
In the module utils directory, the file alicloud_ecs.py identifies and gains playbook params, and provides this params to modules/*.py. In addition, this file implements connection between ansible and Alicloud API via footmark.

## footmark
footmark is a Python package that provides interfaces to Alicloud Web Services, which allows Python developers to write software that makes use of Alicloud ECS.

## roles
There are some playbook that can be used to operate some alicloud services in the roles directory. In every playbook, you need to input some params, and you can view every param description in the modules/*.py.
There are some alicloud modules in the directory library, and some module utils in the module_utils. It can help you use alicloud modules when executing playbook.


### Install Alicloud Modules
Download roles directory in anywhere, and if you want to use new alicloud module, please copy it to the library. The final folder structure after install ecs module:

	- roles
	  - library
	    - alicloud_instance.py
	    - alicloud_disk.py
	    - alicloud_security_group.py
	    - alicloud_vpc.py
	    - alicloud_vswitch.py
	  - module_utils
	    - alicloud_ecs.py
	  - test_ecs.yml
	  - test_vpc.yml

### Execute playbook

* Input your alicloud access-key pairs in the playbook or set environment variable:`ALICLOUD_ACCESS_KEY` and `ALICLOUD_SECRET_KEY`).
* Input others resource params in the playbook.
* Move the playbook to roles and execute ansible-playbook command as follows:

	  $ ansible-playbook test_ecs.yml
	   

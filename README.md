# Ansible ECS Module

[![Build Status](https://travis-ci.org/Click2Cloud/ansible-provider.svg?branch=master)](https://travis-ci.org/Click2Cloud/ansible-provider)

Ansible ECS Module is a new ansible module, and you can manage Alicloud ECS more flexibly and conveniently via it. Next to introduce simply this module.
## lib/ansible/modules/cloud/alicloud
There are several files in the module directory, and these files describe some function that can operate alicloud products.

- `ecs.py`: Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group
- `ecs_ami.py`: Create or Delete User-defined Image
- `ecs_disk.py`: Create, Attach, Detach or Delete a disk in ECS
- `ecs_group.py`: Create, Query or Delete Security Group
- `ecs_slb.py`: Add, Remove, Set and Describe Backend Servers Health
- `ecs_slb_lb.py`: Create, Delete SLB and Listener and Add Backend Server
- `ecs_slb_vsg.py`: Create, Remove, Set VServer Group - Add, Remove and Modify VServer Group Backend Sever
- `ecs_vpc.py`: Create Delete Vpc and Vswitch, Querying Vswitch and VRouter and Adding Route Entry
- `ecs_eip.py`: Request, Bind, Unbind, Modify and Release EIP
- `oss.py`: Create, Delete Bucket and Folder. Upload Files in Bucket, List Bucket objects.
- `rds.py`: Create, Restart, Release and Modify RDS Instance, Create an RDS Read-only Instance, Changing RDS Instance type,
 Switching between Primary and Standby Database, Create Database, Delete database in RDS.
- `rds_account.py`: Create and Delete Account, Resetting Instance password, Resetting account, Granting account permission and Revoking account permission.

## lib/ansible/module_utils/ecsutils
In the utils directory, the file ecs.py identifies and gains playbook params, and provides this params to module/*.py. In addition, this file implements connection between ansible and Alicloud ECS api via footmark.

## lib/ansible/module_utils/ossutils
In the utils directory, the file oss.py identifies and gains playbook params, and provides this params to module/*.py. In addition, this file implements connection between ansible and Alicloud OSS api via footmark.

## footmark
footmark is a Python package that provides interfaces to Alicloud Web Services, which allows Python developers to write software that makes use of Alicloud ECS.

## roles
There are some playbook that can be used to operate ecs in the roles directory. In every playbook, you need to input some params, and you can view every param description in the module/ecs_module.py.
There is ecs module file in the directory library, and you must put library/ecs.py into roles before you execute playbook.


## How to use ECS Module
You can run the following command to install ecsutils:

	$ sudo pip install ecsutils
And if you want to update ecsutils, you can execute command:

	$ sudo pip install ecsutils --upgrade
	
## How to use OSS Module
You can run the following command to install ossutils:

	$ sudo pip install ossutils
And if you want to update ossutils, you can execute command:

	$ sudo pip install ossutils --upgrade

### Install module/ecs.py
Download roles directory in anywhere and make library/ecs.py in the roles. If not, you can put ecs.py into library(if not, make it), and move the library to the roles. The final folder structure after install ecs module:

	- roles
	  - library
	    - ecs.py
	  - start.yml

### Execute playbook
Before you execute playbook, you should input your access-key pairs(`acs_access_key` and `acs_secret_access_key`) in the playbook or set environment variable:`ACS_ACCESS_KEY` and `ACS_SECRET_ACCESS_KEY`. Then input others ecs params in the playbook. Finally, move to roles and execute follow command:

	$ ansible-playbook start.yml

### Package ecsutils
When you modify utils/ecsutils/ecs.py, you need to package and distribute it. First, you need to edit utils/ecsutils/__init__.py and set a new version to '__version__ '. Second execute command as follows:

    # build ecsutils package
    $ python setup.py sdist

    # make sure your environment has installed twine, if not, execute command:
    $ sudo pip install twine

    # distribute new ecsutils
    # upload your project
	$ twine upload dist/<your-ecsutils-package>
Finally, use `--upgrade` to update ecsutils.


### Package ossutils
When you modify utils/ossutils/oss.py, you need to package and distribute it. First, you need to edit utils/ossutils/__init__.py and set a new version to '__version__ '. Second execute command as follows:

    # build ossutils package
    $ python setup.py sdist

    # make sure your environment has installed twine, if not, execute command:
    $ sudo pip install twine

    # distribute new ossutils
    # upload your project
	$ twine upload dist/<your-ossutils-package>
Finally, use `--upgrade` to update ossutils.
	   

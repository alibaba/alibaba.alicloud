# Alibaba Cloud Collection
The Ansible Alibaba Cloud collection includes a variety of Ansible content to help automate the management of Alibaba Cloud instances. This collection is maintained by the Alibaba Cloud team.

<a href="https://shell.aliyun.com/?action=git_open&git_repo=https://code.aliyun.com/labs/tutorial-cli-ansible.git&tutorial=tutorial-zh.md#/" target="try_ansible_in_cloudshell">
  <img src="https://img.alicdn.com/tfs/TB1wt1zq9zqK1RjSZFpXXakSXXa-1066-166.png" width="180" />
</a>

## Python version compatibility

This collection requires Python 3.6 or greater.

## Installing this collection

You can install the Alibaba Cloud collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install alibaba.alicloud

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: alibaba.alicloud
```

A specific version of the collection can be installed by using the `version` keyword in the `requirements.yml` file:

```yaml
---
collections:
  - name: alibaba.alicloud
    version: 1.0.0
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

    pip install requirements.txt

## Using this collection

You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `alibaba.alicloud.ali_vpc`, or you can call modules by their short name if you list the `alibaba.alicloud` collection in the playbook's `collections` keyword:

```yaml
---
	- name: Create a new alicloud VPC resource
	  alibaba.alicloud.ali_vpc:
		state: 'present'
		cidr_block: '{{ vpc_cidr }}'
		vpc_name: '{{ name }}'
		description: '{{ vpc_description }}'
	  register: vpc
```

## plugins/modules
There are several files in the module directory, and these files describe some function that can operate alicloud products.

- `ali_instance.py`: Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group
- `ali_disk.py`: Create, Attach, Detach or Delete a disk in ECS
- `ali_security_group.py`: Create or Delete a Security Group
- `ali_vpc.py`: Create or Delete a Vpc.
- `ali_vswitch.py`: Create or Delete a VSwitch.
- `ali_route_entry.py`: Create or Delete a route entry.
- `ali_slb_lb.py`: Create or Delete a Load balancer.
- `ali_slb_listener.py`: Create or Delete a listener for one Load balancer.
- `ali_slb_server.py`: Add or Remove backend server to/from Load balancer.
- `ali_ess_group.py`: Create or Delete a scaling group.
- `ali_ess_configuration.py`: Create or Delete a scaling configuration.
- `ali_ess_instance.py`: Add or Remove ECS instnaces in a specified scaling group.
- `ali_ess_task.py`: Create or Delete a scheduled task for scaling activity.
- `ali_ess_rule.py`: Create or Delete a scaling rule.
- `ali_eni.py`: Create or Delete a network interface.
- `ali_bucket.py`: Create or Delete an OSS bucket.
- `ali_bucket_object.py`: Upload or Download an object to/from an OSS bucket.

## lib/ansible/module_utils
In the module utils directory, the file alicloud_ecs.py identifies and gains playbook params, and provides this params to modules/*.py. In addition, this file implements connection between ansible and Alicloud API via footmark.

## examples
There are some playbooks to create some alicloud resource or build infrastructure architecture.

### Execute playbook

* Input your alicloud access key in the playbook or set environment variable:`ALICLOUD_ACCESS_KEY` and `ALICLOUD_SECRET_KEY`).
* Input others resource params in the playbook.
* execute ansible-playbook command as follows:

	  $ ansible-playbook xxx.yml
	   
## Refrence

Ansible Document: https://docs.ansible.com/ansible/latest/

Ansible Alicloud: [Docs Details](http://47.88.222.42:8080/ansible-alicloud/latest/modules/list_of_cloud_modules.html)

## Alicloud VPC + VSwitch + Security Group + Instance + Disk Cluster Building

- Requires Ansible 1.2 or newer
- Requires Ansible-Alicloud 1.0.2 or newer
- Requires footmark 1.1.9 or newer


These playbooks build a simple Alicloud VPC cluser based on Ansible provider of Alicloud.
The VPC cluster will contains one VPC, one VSwitch, one Security Group, several Security Group Rules, two Instances and two Disks for Instances.

These playbooks' hosts default to `localhost`. To use, make the file and edit the `hosts` inventory file to include the names or IPs of the servers
you want to deploy.

Then run the playbook, like this:

	ansible-playbook alicloud.yml
	or
	ansible-playbook -i hosts alicloud.yml

The playbooks will create VPC, VSwitch, Secutiry Group, ECS instances and disks. When the run
is complete, you can login in the Alicloud console to check them.

### Notes

Here are some notes before running these playbooks:

- Alicloud_instance module support to create multiple instances one time via parameter 'count'.
- At present, alicloud_instance module can support idempotent only by parameter 'instance_ids', and other modules can support idempotent by their respective ID and name.

### Ideas for Improvement
We would love to see contributions and improvements, so please fork this
repository on GitHub and send us your changes via pull requests.

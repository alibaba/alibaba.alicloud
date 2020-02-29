## Add or Remove tags for resources

- Requires Ansible 2.9 or newer
- Requires Ansible-Alicloud 1.16.1 or newer
- Requires footmark 1.17.1 or newer


These playbooks filter resources and add tags for them.

These playbooks' hosts default to `localhost`. To use, make the file and edit the `hosts` inventory file to include the names or IPs of the servers
you want to deploy.

Then run the playbook, you can add tags like:

```shell
ansible-playbook tags.yml --extra-vars "alicloud_region=cn-hangzhou state=present"
```
Or remove tags like:
```shell
ansible-playbook tags.yml --extra-vars "alicloud_region=cn-hangzhou state=absent"
```

When the run is complete, you can login in the Alicloud console to check them.

### Notes

Here are some notes before running these playbooks:

- When add tags, If tags exist, changed is false.
- When remove tags, If tags not exist, changed is false.

### Ideas for Improvement
We would love to see contributions and improvements, so please fork this
repository on GitHub and send us your changes via pull requests.

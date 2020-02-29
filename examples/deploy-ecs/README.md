## Add or Remove tags for resources

- Requires Ansible 2.9 or newer
- Requires Ansible-Alicloud 1.17.0 or newer
- Requires footmark 1.18.0 or newer


These playbooks Create ECS and Deploy product on them.

These playbooks' hosts default to `localhost`. To use, make the file and edit the `hosts` inventory file to include the names or IPs of the servers
you want to deploy.

### Configuration

export ALICLOUD_INI_PATH=./alicloud.ini

### Usage
Then run the playbook, like this:
    
	ansible-playbook -i hosts deploy.yml -k

When the run is complete, you can see the url.


### Ideas for Improvement
We would love to see contributions and improvements, so please fork this
repository on GitHub and send us your changes via pull requests.

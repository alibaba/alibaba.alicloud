#!/usr/bin/python
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see http://www.gnu.org/licenses/.

from future import absolute_import, division, print_function
metaclass = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview']
}

DOCUMENTATION = """ 
---
module: alicloud_vsg
version_added: "2.4"
short_description: Create, Delete, Set, Modify, Add, Remove, describe Attributes VServerGroup
options:
  state:
    description: The state of the instance after operating.
    required: true
    choices: [ 'present', 'absent', 'list', 'set']
  load_balancer_id:
    description:
        - The unique ID of an Server Load Balancer instance
  vserver_group_name:
    description:
        - Virtual server group name
  bandwidth:
    description:
        - Bandwidth peak of Listener
    choices: [1-1000]
  backend_servers:
    description:
        - List of backend servers that need to be added.
        - '[{"key":"value", "key":"value"}]', keys allowed:
            - ServerId (required:true; default: null, type: string) - The server id is the ECS instance Id.
            - Port (required:true; default: null; choices=[i for i in range(1, 65536)]) -Ports used by back-end servers.
            - Weight (required:true; default: 100; choices=[i for i in range(1, 101)]) -The weight of the back-end server
  vserver_group_id:
    description:
        - Virtual server group ID.
    default: null
  new_backend_servers:
    description:
        - List of backend servers that need to be added.
        - '[{"key":"value", "key":"value"}]', keys allowed:
            - ServerId (required:true; default: null, type: string) - The server id is the ECS instance Id.
            - Port (required:true; default: null; choices=[i for i in range(1, 65536)]) -Ports used by back-end servers.
            - Weight (required:true; default: 100; choices=[i for i in range(1, 101)]) -The weight of the back-end server
  old_backend_servers:
    description:
        - A list of backend servers that need to be removed, such as values that are not present, will be ignored and will not be reported
        - '[{"key":"value", "key":"value"}]', keys allowed:
            - ServerId (required:true; default: null, type: string) - The server id is the ECS instance Id.
            - Port (required:true; default: null; choices=[i for i in range(1, 65536)]) -Ports used by back-end servers.   
"""

EXAMPLES = """
# basic provisioning example to create VServer Group in SLB
- name: Create VServer Group in SLB
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    load_balancer_id: <your-specified-load-balancer>
    vserver_group_name: test
    backend_servers:
       -  ServerId: <your-specified-ECS-instance-id>
          Port: 8080
          Weight: 100
  tasks:
    - name: Create VServer Group in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        vserver_group_name: '{{ vserver_group_name }}'
        backend_servers: '{{ backend_servers }}'
        state: present
      register: result
    - debug: var=result

# basic provisioning example to set VServer Group attribute in SLB
- name: set VServer Group attribute in SLB
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    load_balancer_id: <your-specified-load-balancer>
    vserver_group_name: test
    backend_servers:
       -  ServerId: <your-specified-ECS-instance-id>
          Port: 8080
          Weight: 100
  tasks:
    - name: Set VServer Group attribute in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        vserver_group_name: '{{ vserver_group_name }}'
        backend_servers: '{{ backend_servers }}'
        state: set
      register: result
    - debug: var=result

# basic provisioning example to modify VServer Group in SLB
- name: Modify VServer Group in SLB
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    vserver_group_id: <your-specified-vserver-group-id>
    old_backend_servers:
       -  ServerId: <your-specified-ECS-instance-id>
          Port: 8080
    new_backend_servers:
       -  ServerId: <your-specified-ECS-instance-id>
          Port: 8080
          Weight: 100
  tasks:
    - name: modify VServer Group in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vserver_group_id: '{{ vserver_group_id }}'
        old_backend_servers: '{{ old_backend_servers }}'
        new_backend_servers: '{{ new_backend_servers }}'
        state: set
      register: result
    - debug: var=result

# basic provisioning example to add VServer Group Backend Servers in SLB
- name: Add VServer Group Backend Servers in SLB
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    vserver_group_id: <your-specified-vserver-group-id>
    backend_servers:
       -  ServerId: <your-specified-ECS-instance-id>
          Port: 8080
          Weight: 100
  tasks:
    - name: Add VServer Group Backend Servers in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vserver_group_id: '{{ vserver_group_id }}'
        backend_servers: '{{ backend_servers }}'
        state: present
      register: result
    - debug: var=result

# basic provisioning example to remove VServer Group Backend Servers in SLB
- name: remove VServer Group Backend Servers in SLB
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    vserver_group_id: <your-specified-vserver-group-id>
    backend_servers:
       -  ServerId: <your-specified-ECS-instance-id>
          Port: 8080
  tasks:
    - name: remove VServer Group Backend Servers in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vserver_group_id: '{{ vserver_group_id }}'
        backend_servers: '{{ backend_servers }}'
        state: absent
      register: result
    - debug: var=result

# basic provisioning example to describe VServer Group in SLB
- name: describe VServer Group
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    vserver_group_id: <your-specified-vserver-group-id>
  tasks:
    - name: Describe VServer Group in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vserver_group_id: '{{ vserver_group_id }}'
        state: list
      register: result
    - debug: var=result

# basic provisioning example to delete VServer Group in SLB
- name: Delete VServer Group
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: ap-southeast-1
    vserver_group_id: <your-specified-vserver-group-id>
  tasks:
    - name: Delete VServer Group in SLB
      ecs_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vserver_group_id: '{{ vserver_group_id }}'
        state: absent
      register: result
    - debug: var=result    
"""

RETURN = '''
vserver_group:
    description:
        - The info of vserver_group
    returned: when success
    type: dict
    sample: {
        "backend_servers": {
            "backend_server": [
                {
                    "port": 80, 
                    "server_id": "i-2ze3ajpeq3y80w4lt4jr", 
                    "weight": 100
                }
            ]
        }, 
        "vserver_group_id": "rsp-2zejxvoxensk1", 
        "vserver_group_name": "Group123"
    }
'''

import time
import sys
from ast import literal_eval
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, slb_connect


HAS_ECS = False
HAS_FOOTMARK = False

try:
    from footmark.exception import SLBResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(obj):
    """
    get info from vsg object
    :param obj: vsg obj
    :return: res: info of vsg
    """
    res = {}
    res['vserver_group_id'] = obj.vserver_group_id
    if hasattr(obj, 'backend_servers'):
        res['backend_servers'] = obj.backend_servers
    if hasattr(obj, 'vserver_group_name'):
        res['vserver_group_name'] = obj.vserver_group_name
    return res

def main():
    if HAS_FOOTMARK is False:
        module.fail_json("Footmark required for this module")

    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(type='str', required=True, choices=['present', 'absent', 'list', 'set']),
        load_balancer_id=dict(type='str'),
        vserver_group_name=dict(type='str'),
        backend_servers=dict(type='list'),
        vserver_group_id=dict(type='str', aliases=['id']),
        old_backend_servers=dict(type='list'),
        new_backend_servers=dict(type='list')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    slb = slb_connect(module)
    state = module.params['state']
    load_balancer_id = module.params['load_balancer_id']
    vserver_group_name = module.params['vserver_group_name']
    backend_servers = module.params['backend_servers']
    vserver_group_id = module.params['vserver_group_id']
    old_backend_servers = module.params['old_backend_servers']
    new_backend_servers = module.params['new_backend_servers']
    changed = False
    current_vserver_group = None
    
    if vserver_group_id:
        current_vserver_group = slb.describe_vserver_group_attribute(vserver_group_id)

    if state == "present":
        if current_vserver_group:
            obj = current_vserver_group.add_backend_servers(backend_servers)
            changed = True
        else:
            current_vserver_group = slb.create_vserver_group(load_balancer_id, vserver_group_name, backend_servers)
            changed = True
        module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group.describe_attribute()))
    if not current_vserver_group:
        module.fail_json(msg="The specified vserver group is not exist. Please check your vserver_group_id and try again.")
    elif state == "set":
        if vserver_group_name or backend_servers:
            obj = current_vserver_group.set_attribute(vserver_group_name, backend_servers)
            changed = True
            module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group.describe_attribute()))
        elif old_backend_servers or new_backend_servers:
            obj = current_vserver_group.modify_backend_servers(old_backend_servers, new_backend_servers)
            changed = True
            module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group.describe_attribute()))
        else:
            module.fail_json(msg="illegal operation, Please check your params and try again. state: {0}".format(state))
    elif state == "list":
        changed = True
        module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group))
    elif state == 'absent':
        if backend_servers:
            obj = current_vserver_group.remove_backend_servers(backend_servers)
            changed = True
            module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group.describe_attribute()))
        else:
            changed = current_vserver_group.delete()
            module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group))
            

if __name__ == "__main__":
    main()

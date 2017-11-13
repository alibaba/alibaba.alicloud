#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
#  This file is part of Ansible
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_slb_vsg
version_added: "2.5"
short_description: Create, Delete VServerGroup and Modify its name or backend servers.
description:
  - Create, Delete VServerGroup and Modify its name or backend servers.
options:
    state:
      description:
        - The state of the instance after operating.
      default: 'present'
      choices: [ 'present', 'absent', 'list']
    load_balancer_id:
      description:
        - The unique ID of an Server Load Balancer instance, It is required when need to create a new vserver group.
    vserver_group_name:
      description:
        - Virtual server group name
      aliases: [ 'group_name' ]
    backend_servers:
      description:
        - List of backend servers that need to be added.
      suboptions:
        instance_id:
          description:
            - The ID of backend server.
          required: true
        port:
          description:
            - Port used to backend server
          required: true
          choices: [1~65536]
        weight:
          description:
            - The weigth of the backend server
          default: 100
          choices: [1~101]
    vserver_group_id:
      description:
        - Virtual server group id. It is required when need to operate an existing vserver group.
      aliases: [ 'group_id' ]
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
  - "Liu Qiang"
'''

EXAMPLES = '''
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
      - instance_id: <your-specified-ECS-instance-id>
        port: 8080
        weight: 100
  tasks:
    - name: Create VServer Group in SLB
      alicloud_slb_vsg:
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
      - instance_id: <your-specified-ECS-instance-id>
        port: 8080
        weight: 100
  tasks:
    - name: Set VServer Group attribute in SLB
      alicloud_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        vserver_group_name: '{{ vserver_group_name }}'
        backend_servers: '{{ backend_servers }}'
        state: present
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
      - instance_id: <your-specified-ECS-instance-id>
        port: 8080
        weight: 100
  tasks:
    - name: Add VServer Group Backend Servers in SLB
      alicloud_slb_vsg:
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
      - instance_id: <your-specified-ECS-instance-id>
        port: 8080
  tasks:
    - name: remove VServer Group Backend Servers in SLB
      alicloud_slb_vsg:
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
      alicloud_slb_vsg:
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
      alicloud_slb_vsg:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vserver_group_id: '{{ vserver_group_id }}'
        state: absent
      register: result
    - debug: var=result
'''

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
    res = {'vserver_group_id': obj.vserver_group_id}

    if hasattr(obj, 'backend_servers'):
        res['backend_servers'] = obj.backend_servers
    if hasattr(obj, 'vserver_group_name'):
        res['vserver_group_name'] = obj.vserver_group_name
    return res


def convert_to_utf8(obj):
    if sys.version_info.major == 3:
        return obj
    if isinstance(obj, dict):
        res = {}
        for key, value in obj.iteritems():
            res = dict(res, **{convert_to_utf8(key): convert_to_utf8(value)})
        return res
    elif isinstance(obj, list):
        res = []
        for i in obj:
            res.append(convert_to_utf8(i))
        return res
    elif type(obj) not in [int, float, bool, complex, long]:
        return obj.encode('utf-8')
    return obj


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(type='str', default='present', choices=['present', 'absent', 'list']),
        load_balancer_id=dict(type='str'),
        vserver_group_name=dict(type='str', aliases=['group_name']),
        backend_servers=dict(type='list'),
        vserver_group_id=dict(type='str', aliases=['group_id']),
        old_backend_servers=dict(type='list'),
        new_backend_servers=dict(type='list')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_slb_vsg.')

    slb = slb_connect(module)
    state = module.params['state']
    load_balancer_id = module.params['load_balancer_id']
    vserver_group_name = module.params['vserver_group_name']
    backend_servers = module.params['backend_servers']
    vserver_group_id = module.params['vserver_group_id']
    changed = False
    current_vserver_group = None

    if vserver_group_id:
        try:
            current_vserver_group = slb.describe_vserver_group_attribute(vserver_group_id)
        except Exception as e:
            module.fail_json(msg=str("Unable to describe vserver group attribute, error:{0}".format(e)))
    if state == "present":
        if current_vserver_group:
            set_data = []
            add_data = []
            if backend_servers:
                server_info = {}
                decode_infos = convert_to_utf8(current_vserver_group.backend_servers)
                for info in decode_infos['backend_server']:
                    server_info[info['port']] = info
                for server in backend_servers:
                    if server['port'] in server_info.keys():
                        if server_info[server['port']]['weight'] != server['weight']:
                            set_data.append(server)
                    else:
                        add_data.append(server)
            if set_data or vserver_group_name:
                try:
                    current_vserver_group.set_attribute(backend_servers=set_data, vserver_group_name=vserver_group_name)
                except Exception as e:
                    module.fail_json(msg=str("Unable to set vserver group attribute, error:{0}".format(e)))
            if add_data:
                try:
                    current_vserver_group.add_backend_servers(backend_servers=add_data)
                except Exception as e:
                    module.fail_json(msg=str("Unable to add vserver group backend server, error:{0}".format(e)))
            try:
                current_vserver_group = slb.describe_vserver_group_attribute(vserver_group_id)
            except Exception as e:
                module.fail_json(msg=str("Unable to describe vserver group attribute, error:{0}".format(e)))
            module.exit_json(changed=True, vserver_group=get_info(current_vserver_group))
        else:
            try:
                current_vserver_group = slb.create_vserver_group(load_balancer_id, vserver_group_name, backend_servers)
            except Exception as e:
                module.fail_json(msg=str("Unable to create vserver group error:{0}".format(e)))
            module.exit_json(changed=True, vserver_group=get_info(current_vserver_group))
    if not current_vserver_group:
        module.fail_json(msg="The specified vserver group is not exist. Please check your vserver_group_id and try again.")
    elif state == "list":
        module.exit_json(changed=True, vserver_group=get_info(current_vserver_group))
    elif state == 'absent':
        if backend_servers:
            try:
                current_vserver_group = current_vserver_group.remove_backend_servers(backend_servers)
            except Exception as e:
                module.fail_json(msg=str("Unable to remove vserver group backend server, error:{0}".format(e)))
            module.exit_json(changed=True, vserver_group=get_info(current_vserver_group))
        else:
            try:
                changed = current_vserver_group.delete()
            except Exception as e:
                module.fail_json(msg=str("Unable to delete vserver group, error:{0}".format(e)))
            module.exit_json(changed=changed, vserver_group=get_info(current_vserver_group))


if __name__ == '__main__':
    main()

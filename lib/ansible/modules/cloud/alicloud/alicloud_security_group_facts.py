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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_security_group_facts
version_added: "2.4"
short_description: Gather facts on security group of Alibaba Cloud ECS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the ECS security group itself.

options:
    group_ids:
      description:
        - A list of ECS security group IDs.
      aliases: [ "ids"]
    vpc_id:
      description:
        - Id of vpc to list security groups.
    names:    
    description:
        - Name of the security group.
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''# Fetch security group details according to setting different filters
- name: Fetch security group example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    vpc_id: vpc-2zegusms7jwd94lq7ix8o
    names: 
      - sg-j6cgf3gifygjt94zivku   
    group_ids:
      - sg-2ze28n1vj1iqztxp7p6h
  tasks:
    - name: Find all security groups in the specified region
      alicloud_security_group_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
      register: security_group_by_region
    - debug: var=security_group_by_region

    - name: Find all security groups by group ids
      alicloud_security_group_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        ids: '{{ group_ids }}'
      register: security_group_by_id
    - debug: var=security_group_by_id

    - name: Find all security groups by vpc ids
      alicloud_security_group_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        vpc_id: '{{ vpc_id }}'
      register: security_group_by_vpc_id
    - debug: var=security_group_by_vpc_id

    - name: Find all security groups by group ids and vpc id
      alicloud_security_group_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        ids: '{{ group_ids }}'
        vpc_id: '{{ vpc_id }}'
      register: security_group_by_id_and_vpc_id
    - debug: var=security_group_by_id_and_vpc_id
    
    - name: Find all security groups by name
      alicloud_security_group_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        names: '{{ names }}'
      register: security_group_by_vpc_id
    - debug: var=security_group_by_vpc_id    

    - name: Find all security groups by group ids, vpc id and name 
      alicloud_security_group_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_ids: '{{ group_ids }}'
        vpc_id: '{{ vpc_id }}'
        names: '{{ names }}'
      register: security_group_by_id_and_vpc_id
    - debug: var=security_group_by_id_and_vpc_id
'''

RETURN = '''
group_ids:
    description: list IDs of security groups
    returned: when list
    type: list
    sample: [ "sg-2ze12578be1ls4wcjhfd", "sg-2ze28n1vj1iqztxp7p6h" ]
security_groups:
    description: Details about the security groups that were created
    returned: when success
    type: list
    sample: [
        {
            "description": "security group of ACS Cluster c50f7bbd5412746beaf77eed3f3695703",
            "id": "sg-2ze12578be1ls4wcjhfd",
            "name": "alicloud-cs-auto-created-security-group-c50f7bbd5412746beaf77eed3f3695703",
            "region_id": "cn-beijing",
            "rules": [
                {
                    "create_time": "2017-10-11T10:20:11Z",
                    "description": "",
                    "dest_cidr_ip": "",
                    "dest_group_id": "",
                    "dest_group_name": "",
                    "dest_group_owner_account": "",
                    "direction": "ingress",
                    "ip_protocol": "ALL",
                    "nic_type": "intranet",
                    "policy": "Accept",
                    "port_range": "-1/-1",
                    "priority": 1,
                    "source_cidr_ip": "0.0.0.0/0",
                    "source_group_id": "",
                    "source_group_name": "",
                    "source_group_owner_account": ""
                },
                {
                    "create_time": "2017-10-11T09:34:23Z",
                    "description": "",
                    "dest_cidr_ip": "",
                    "dest_group_id": "",
                    "dest_group_name": "",
                    "dest_group_owner_account": "",
                    "direction": "ingress",
                    "ip_protocol": "ICMP",
                    "nic_type": "intranet",
                    "policy": "Accept",
                    "port_range": "-1/-1",
                    "priority": 1,
                    "source_cidr_ip": "0.0.0.0/0",
                    "source_group_id": "",
                    "source_group_name": "",
                    "source_group_owner_account": ""
                }
            ],
            "tags": {},
            "vpc_id": "vpc-2zegusms7jwd94lq7ix8o"
        },
        {
            "description": "System created security group.",
            "id": "sg-2ze28n1vj1iqztxp7p6h",
            "name": "sg-2ze28n1vj1iqztxp7p6h",
            "region_id": "cn-beijing",
            "rules": [
                {
                    "create_time": "2017-09-11T21:19:35Z",
                    "description": "",
                    "dest_cidr_ip": "",
                    "dest_group_id": "",
                    "dest_group_name": "",
                    "dest_group_owner_account": "",
                    "direction": "ingress",
                    "ip_protocol": "TCP",
                    "nic_type": "intranet",
                    "policy": "Accept",
                    "port_range": "5000/5000",
                    "priority": 1,
                    "source_cidr_ip": "0.0.0.0/0",
                    "source_group_id": "",
                    "source_group_name": "",
                    "source_group_owner_account": ""
                },
                {
                    "create_time": "2017-09-11T21:19:23Z",
                    "description": "",
                    "dest_cidr_ip": "",
                    "dest_group_id": "",
                    "dest_group_name": "",
                    "dest_group_owner_account": "",
                    "direction": "ingress",
                    "ip_protocol": "TCP",
                    "nic_type": "intranet",
                    "policy": "Accept",
                    "port_range": "9090/9090",
                    "priority": 1,
                    "source_cidr_ip": "0.0.0.0/0",
                    "source_group_id": "",
                    "source_group_name": "",
                    "source_group_owner_account": ""
                }
            ],
            "tags": {},
            "vpc_id": "vpc-2zegusms7jwd94lq7ix8o"
        }
    ]
total:
    description: The number of all security groups after operating ecs security group.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_group_detail(group):
    """
    Parse security group detail information.
    returns it as a dictionary
    """
    return {'id': group.id, 'name': group.name, 'description': group.description, 'region_id': group.region_id,
            'tags': group.tags, 'vpc_id': group.vpc_id,
            'rules': group.rules
            }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        vpc_id=dict(type='str'),
        group_ids=dict(type='list', aliases=['ids']),
        names=dict(type='list')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    ecs = ecs_connect(module)

    vpc_id = module.params['vpc_id']
    group_ids = module.params['group_ids']
    names = module.params['names']

    changed = False
    result = []

    if group_ids and (not isinstance(group_ids, list) or len(group_ids)) < 1:
        module.fail_json(msg='group_ids should be a list of security group, aborting')

    if names and (not isinstance(names, list) or len(names)) < 1:
        module.fail_json(msg='names should be a list of security group names, aborting')

    try:
        security_groups = ecs.get_all_security_groups(group_ids=group_ids, vpc_id=vpc_id)
        group_ids = []
        for security_group in security_groups:
            result.append(get_group_detail(security_group))
            group_ids.append(security_group.id)

        if names:
            for name in names:
                security_groups = ecs.get_all_security_groups(name=name)
                for security_group in security_groups:
                    result.append(get_group_detail(security_group))
                    group_ids.append(security_group.id)

    except ECSResponseError as e:
        module.fail_json(msg='Error in get_all_security_groups: %s' % str(e))

    module.exit_json(changed=changed, group_ids=group_ids, security_groups=result, total=len(result))


if __name__ == '__main__':
    main()

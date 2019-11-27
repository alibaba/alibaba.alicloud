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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_rds_instance_info
version_added: "1.5.0"
short_description: Gather facts on database instance of Alibaba Cloud RDS.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the RDS instance itself.

options:
    db_instance_id:
      description:
        - RDS database instance id.
      aliases: [ "instance_id" ]
    engine:
      description:
        - Type of the database.
    dbinstance_type:
      description:
        - Instance type.
    instance_network_type:
      description:
        - Instance network type.
    connection_mode:
      description:
        - Instance connection mode.
    tags:
      description:
        - Database tags.
    get_netinfo:
      description:
        - if True, return db instance's netinfo. otherwise return rds db instances
    name_prefix:
      description:
        - Use instance name prefix to filter rds.        
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch database instance details according to setting different filters
- name: fetch database instance details example
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    engine: MySQL
    dbinstance_type: Temp
    instance_network_type: Classic
    connection_mode: Safe
    tags:  
      rds: '01'
    instance_ids:
      - rm-dj163498yvlgy80ug
  tasks:
    - name: Find all database instance in the specified region
      ali_rds_instance_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
      register: all_db_instance
    - debug: var=all_db_instance

    - name: Find all database instance in the specified region based on instance ids
      ali_rds_instance_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
      register: db_instance_by_ids
    - debug: var=db_instance_by_ids
    
    - name: Find all database instance in the specified region based on database instance type
      ali_rds_instance_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'        
        engine: '{{ engine }}'
      register: db_instance_by_dbtype
    - debug: var=db_instance_by_dbtype   
     
    - name: Find all database instance in the specified region based on instance type
      ali_rds_instance_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'        
        dbinstance_type: '{{ dbinstance_type }}'
      register: db_instance_by_type
    - debug: var=db_instance_by_type  
      
    - name: Find all database instance in the specified region based on instance network type
      ali_rds_instance_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'        
        instance_network_type: '{{ instance_network_type }}'
      register: db_instance_by_network_type
    - debug: var=db_instance_by_network_type  
      
    - name: Find all database instance in the specified region based on instance connection mode and tags
      ali_rds_instance_info:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'        
        connection_mode: '{{ connection_mode }}'
        tags: '{{ tags }}'
      register: db_instance_by_connection_mode
    - debug: var=db_instance_by_connection_mode          
'''

RETURN = '''
instance_ids:
    description: List all database instance's id after operating RDS database instances.
    returned: when success
    type: list
    sample:  [ "rm-dj1d7a046kur7syix", "rm-dj164ju77728joefu" ]
rds_db_instances:
    description: Details about the rds database instances that were created.
    returned: when success
    type: list
    sample: [
        {
            "connection_mode": "Safe",
            "create_time": "2017-11-07T18:47Z",
            "dbinstance_class": "rds.mysql.t1.small",
            "dbinstance_id": "rm-dj1d7a046kur7syix",
            "dbinstance_net_type": "Intranet",
            "dbinstance_status": "Running",
            "dbinstance_type": "Primary",
            "engine": "MySQL",
            "engine_version": "5.6",
            "expire_time": "",
            "ins_id": 1,
            "instance_network_type": "Classic",
            "lock_mode": "Unlock",
            "lock_reason": "",
            "mutri_orsignle": false,
            "pay_type": "Postpaid",
            "read_only_dbinstance_ids": {
                "read_only_dbinstance_id": []
            },
            "region_id": "cn-beijing",
            "resource_group_id": "rg-acfmv53ndviljcy",
            "zone_id": "cn-beijing-a"
        },
        {
            "connection_mode": "Safe",
            "create_time": "2017-11-07T18:23Z",
            "dbinstance_class": "rds.mysql.t1.small",
            "dbinstance_id": "rm-dj164ju77728joefu",
            "dbinstance_net_type": "Intranet",
            "dbinstance_status": "Running",
            "dbinstance_type": "Primary",
            "engine": "MySQL",
            "engine_version": "5.6",
            "expire_time": "",
            "ins_id": 1,
            "instance_network_type": "Classic",
            "lock_mode": "Unlock",
            "lock_reason": "",
            "mutri_orsignle": false,
            "pay_type": "Postpaid",
            "read_only_dbinstance_ids": {
                "read_only_dbinstance_id": []
            },
            "region_id": "cn-beijing",
            "resource_group_id": "rg-acfmv53ndviljcy",
            "zone_id": "cn-beijing-a"
        }
    ]
total:
    description: The number of all database instances after operating RDS database instances.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, rds_connect, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import RDSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        db_instance_id=dict(type='str', aliases=['instance_id']),
        engine=dict(type='str'),
        db_instance_type=dict(type='str', aliases=['instance_type']),
        instance_network_type=dict(type='str'),
        connection_mode=dict(type='str'),
        tags=dict(type='dict'),
        get_netinfo=dict(type='bool', default=False),
        name_prefix=dict(type='str')
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    rds = rds_connect(module)
    get_netinfo = module.params['get_netinfo']
    db_instance_id = module.params['db_instance_id']
    name_prefix = module.params['name_prefix']

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    result = []
    ids = []
    if get_netinfo:
        try:
            for info in rds.describe_d_b_instance_net_info(**module.params):
                result.append(info.read())
            ids.append(db_instance_id)
            module.exit_json(changed=False, db_instance_ids=ids, db_instances_netinfo=result)
        except Exception as e:
            module.fail_json(msg="Unable to describe rds db instance, and got an error: {0}.".format(e))

    try:
        for rds_instance in rds.describe_d_b_instances(**module.params):
            if name_prefix and rds_instance.db_instance_description != name_prefix:
                continue
            result.append(rds_instance.read())
            ids.append(rds_instance.dbinstance_id)
        module.exit_json(changed=False, db_instance_ids=ids, rds_db_instances=result, total=len(result))
    except Exception as e:
        module.fail_json(msg="Unable to describe rds db instance, and got an error: {0}.".format(e))


if __name__ == '__main__':
    main()

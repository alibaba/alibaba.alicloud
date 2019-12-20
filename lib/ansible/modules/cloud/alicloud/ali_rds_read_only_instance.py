#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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
module: ali_rds_read_only_instance
version_added: "2.9"
short_description: Create RDS read only Instance in Alibaba Cloud.
description:
    - Create readonly instance for RDS Instance.
    - This module does not support idempotence
options:
  zone_id:
    description:
      - Aliyun availability zone ID in which to launch the instance.
        If it is not specified, it will be allocated by system automatically.
    aliases: ['alicloud_zone']
  engine_version:
    description:
      - The version of the database.
      - MySQL (5.5 | 5.6 | 5.7 | 8.0)
      - SQL Server (2008r2 | 2012 | 2012_ent_ha | 2012_std_ha | 2012_web | 2016_ent_ha | 2016_std_ha | 2016_web | 2017_ent)
      - PostgreSQL (9.4 | 10.0)
      - PPAS (9.3 | 10.0)
      - MariaDB (10.3)
      - see more (https://www.alibabacloud.com/help/doc-detail/26228.htm)
  db_instance_class:
    description:
      - The instance type (specifications). For more information, see(https://www.alibabacloud.com/help/doc-detail/26312.htm).
    aliases: ['instance_class']
  db_instance_storage:
    description:
      - The storage capacity of the instance. Unit(GB). This value must be a multiple of 5. For more information see(https://www.alibabacloud.com/help/doc-detail/26312.htm).
    aliases: ['instance_storage']
  db_instance_net_type:
    description:
      - Instance of the network connection type (Internet on behalf of the public network, Intranet on behalf of the private network）
        Required when C(state=present).
    aliases: ['instance_net_type']
    choices: ["Internet", "Intranet"]
  db_instance_description:
    description:
      - The instance name. It starts with a letter and contains 2 to 255 characters, including letters, digits, underscores (_), and hyphens (-).
        It cannot start with http:// or https://.
    aliases: ['description']
  pay_type:
    description:
      - The billing method of the instance.
    choices: ["PostPaid", "PrePaid"]
  vswitch_id:
    description:
      - The ID of the VSwitch. Separate multiple IDs with commas (,).
  private_ip_address:
    description:
      - The intranet IP address of the instance. It must be within the IP address range provided by the switch. 
        By default, the system automatically assigns an IP address based on the VPCId and VSwitchId.
  db_instance_id:
    description:
      - Instance id.
      - The unique identifier of the instance. 
    aliases: ['instance_id']
    required: True
  resource_group_id:
    description:
      - The id of the resource group.
author:
    - "Li Xue"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.16.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
- name: Changed. Create read only db instance
  ali_rds_instance:
    db_instance_id: '{{ db_instance_id }}'
    zone_id: cn-beijing-b
    db_instance_class: rds.mysql.s1.small
    db_instance_storage: 30
    pay_type: PostPaid
    engine_version: 5.6
'''

RETURN = '''
instances:
    description: Describe the info after create rds read only instance.
    returned: always
    type: complex
    contains:
        db_instance_id:
            description: The ID of the read only instance.
            returned: always
            type: string
            sample: rr-uf6wjk5xxxxxxx
        id:
            description: alias of 'db_instance_id'.
            returned: always
            type: string
            sample: rr-uf6wjk5xxxxxxx
        connection_string:
            description: The endpoint URL of the read-only instance..
            returned: always
            type: string
            sample: rr-xxxxx.mysql.rds.aliyuncs.com
        port:
            description: The internal port of the read-only instance.
            returned: always
            type: string
            sample: 3306
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, rds_connect, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        zone_id=dict(type='str', aliases=['alicloud_zone']),
        engine_version=dict(type='str'),
        db_instance_description=dict(type='str', aliases=['description']),
        security_ip_list=dict(type='str', aliases=['security_ips']),
        pay_type=dict(type='str', choices=["PostPaid", "PrePaid"]),
        vswitch_id=dict(type='str'),
        private_ip_address=dict(type='str'),
        db_instance_id=dict(type='str', aliases=['instance_id'], required=True),
        tags=dict(type='dict'),
        purge_tags=dict(type='bool', default=False),
        db_instance_class=dict(type='str', aliases=['instance_class']),
        db_instance_storage=dict(type='int', aliases=['instance_storage']),
        resource_group_id=dict(type='str')
    ))
    modules = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        modules.fail_json(msg="Package 'footmark' required for the module ali_rds_instance.")

    rds = rds_connect(modules)
    vpc = vpc_connect(modules)

    vswitch_id = modules.params['vswitch_id']
    pay_type = modules.params['pay_type']
    if pay_type:
        modules.params['pay_type'] = pay_type.capitalize()
    changed = False
    if vswitch_id:
        modules.params['instance_network_type'] = 'VPC'
        try:
            vswitch_obj = vpc.describe_vswitch_attributes(vswitch_id=vswitch_id)
            if vswitch_obj:
                modules.params['vpc_id'] = vswitch_obj.vpc_id
        except Exception as e:
            modules.fail_json(msg=str("Unable to get vswitch, error:{0}".format(e)))

    try:
        modules.params['client_token'] = "Ansible-Alicloud-%s-%s" % (hash(str(modules.params)), str(time.time()))
        current_instance = rds.create_read_only_db_instance(**modules.params)
        modules.exit_json(changed=changed, instances=current_instance.read())
    except Exception as e:
        modules.fail_json(msg=str("Unable to create rds read only instance error: {0}".format(e)))


if __name__ == '__main__':
    main()


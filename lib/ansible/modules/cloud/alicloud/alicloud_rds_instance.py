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
module: alicloud_rds_instance
version_added: "2.5"
short_description: Create, Restart or Terminate an Instance in RDS.
description:
    - Create, restart, modify or terminate rds instances.
options:
  state:
    description:
      - The state of the instance after operating.
    default: 'present'
    choices: [ 'present', 'restart', 'absent' ]
    aliases: ['status']
  alicloud_zone:
    description:
      - Aliyun availability zone ID in which to launch the instance.
        If it is not specified, it will be allocated by system automatically.
    aliases: ['zone_id', 'zone']
  engine:
    description:
      - Database type. Required when C(state=present).
    choices: [ 'MySQL', 'SQLServer', 'PostgreSQL', 'PPAS' ]
  engine_version:
    description:
      - The database version number, as follows:
        MySQL: 5.5 / 5.6 / 5.7;
        SQLServer: 2008r2 / 2012;
        PostgreSQL: 9.4;
        PPAS: 9.3.
        Required when C(state=present).
  instance_type:
    description:
      - Instance specification. Required when C(state=present).
    aliases: ['db_instance_class']
  instance_storage:
    description:
      - Customize storage, range:
        MySQL / PostgreSQL / PPAS dual high-availability version of [5,2000];
        MySQL 5.7 standalone basic version is [20,1000];
        SQL Server 2008R2 is [10,2000];
        SQL Server 2012 standalone basic version of [20,2000];
        Increased every 5G. Unit: GB.
        Required when C(state=present).
    aliases: ['db_instance_storage']
  instance_net_type:
    description:
      - Instance of the network connection type: Internet on behalf of the public network, Intranet on behalf of the private network.
        Required when C(state=present).
    choices: ["Internet", "Intranet"]
    aliases: ['db_instance_net_type']
  description:
    description:
      - Instance description or memo information, no more than 256 bytes;
        Note: You can not start with http: //, https: //. Start with Chinese and English letters.
        Can contain Chinese, English characters, "_", "-", the number of characters length 2 ~ 256.
    aliases: ['db_instance_description']
  security_ips:
    description:
      - Allow access to the IP list of all databases under this instance,
        separated by commas, not repeatable, up to 1000;
        Supported formats:%, 0.0.0.0/0,10.23.12.24 (IP),
        or 10.23.12.24/24 (CIDR mode , No class interdomain routing,
        / 24 indicates the length of the prefix in the address,
        the range [1,32]) where 0.0.0.0 / 0, that does not limit
        Required when C(state=present).
  instance_charge_type:
    description:
      - Type of payment. Postpaid: postpaid instance; Prepaid: prepaid instance. Required when C(state=present).
    choices: [ "Postpaid", "Prepaid" ]
  period:
    description:
      - The charge duration of the instance. Required when C(instance_charge_type=PrePaid).
    choices: [1~9,12,24,36]
    default: 1
  connection_mode:
    description:
      - Performance is standard access mode; Safty is a high security access mode; default is RDS system allocation.
    choices: ["Performance", "Safty"]
  vswitch_id:
    description:
      - Vswitch id
  private_ip_address:
    description:
      - Users can specify VSvitchId under vpcIp, if not input, the system automatically assigned.
  instance_id:
    description:
      - Instance id, the unique identifier if the instance. Required when C(state in ["present", "absent", "restart"])
  aliases: ['db_instance_id']
  tags:
    description:
      - The query is bound to an instance of this tag,
        the incoming value format is Json string,
        including TagKey and TagValue,
        TagKey can not be empty,
        TagValue can be empty.
        Format example: {"key1": "value1"}
  page_size:
    description:
      - Number of records per page.
    choices: [30,50,100]
    default: 30
  page_number:
    description:
      - Page number greater than 0, and does not exceed the maximum value of Integer.
    type: int
    default: 1
  auto_renew_period:
    description:
      - Automatic renewal period. Required when C(auto_renew='True')
    choices: [1, 2, 3, 6, 12]
  auto_renew:
    description:
      - Automatic renewal. Required when C(auto_renew != None)
    type: bool
  public_connection_string_prefix:
    description:
      - The prefix of the outer network connection string. Required when C(state in ['present', 'absent']).
  dest_connection_string_prefix:
    description:
      - The prefix of the outer network connection string. Required when C(state in ['present', 'absent']).
  private_connection_string_prefix:
    description:
      - The prefix of the outer network connection string. Required when C(state in ['present', 'absent']).
  public_port:
    description:
      - Port of public net work.
  private_port:
    description:
      - Port of private net work.
  dest_port:
    description:
      - Port to replace the old.
  current_connection_string:
    description:
      - Instance of a current connection string. Required when C(current_connection_string != None)
author:
    - "liu Qiang"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# basic provisioning example to create rds instance
- name: create rds instance
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: create instance
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        engine: MySQL
        engine_version: 5.6
        instance_class: rds.mysql.t1.small
        instance_storage: 30
        instance_net_type: Internet
        security_ips: 10.23.12.24/24
        instance_charge_type: Postpaid

# basic provisioning example to modify instance auto renewal attribute
- name: modify instance auto renewal attribute
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: modify instance auto renewal attribute
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        instance_id: rm-2ze3083kmle92v50t
        auto_renew: False

# basic provisioning example to allocate instance private connection string
- name: allocate instance private connection string
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: allocate instance private connection string
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        private_connection_string_prefix: pirave-89asd
        instance_id: rm-2ze3083kmle92v50t

# basic provisioning example to allocate instance public connection string
- name: allocate instance public connection string
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: allocate instance public connection string
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        public_connection_string_prefix: pirave-89asd
        public_port: 3212
        instance_id: rm-2ze3083kmle92v50t

# basic provisioning example to modify instance current connection string
- name: modify instance current connection string
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: modify instance current connection string
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: present
        current_connection_string: rm-2ze3083kmle92v50t.mysql.rds.aliyuncs.com
        dest_connection_string_prefix: adsad-ewq4f
        dest_port: 4321
        instance_id: rm-2ze3083kmle92v50t

# basic provisioning example to release instance public connection string
- name: release instance public connection string
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: release instance public connection string
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: absent
        current_connection_string: rm-2ze3083kmle92v50t.mysql.rds.aliyuncs.com
        instance_id: rm-2ze3083kmle92v50t

# basic provisioning example to restart rds instacne
- name: restart rds instacne
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: restart rds instacne
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: restart
        instance_id: rm-2ze3083kmle92v50t

# basic provisioning example to release rds instacne
- name: release rds instacne
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
  tasks:
    - name: release rds instacne
      alicloud_rds_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: absent
        instance_id: rm-2ze3083kmle92v50t
'''

RETURN = '''
instance:
  description: Describe the info after operating rds instance.
  returned: when success
  type: dict
  sample: {
      "connection_string": "rm-2ze3083kmle92v50t.mysql.rds.aliyuncs.com",
      "db_instance_id": "rm-2ze3083kmle92v50t",
      "db_instance_status": "Running",
      "db_instance_storage": 30,
      "db_instance_type": "Primary",
      "db_instance_net_type": "Intranet",
      "engine": "MySQL",
      "engine_version": "5.6",
  }
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


def get_info(obj):
    if not obj:
        return None
    return dict(db_instance_id=obj.dbinstance_id,
                db_instance_status=obj.dbinstance_status,
                db_instance_storage=obj.dbinstance_storage,
                db_instance_type=obj.dbinstance_type,
                db_instance_net_type=obj.dbinstance_net_type,
                engine=obj.engine,
                engine_version=obj.engine_version,
                connection_string=obj.connection_string)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default="present", choices=["present", "absent", "restart"], alias=['status']),
        alicloud_zone=dict(type='str', aliases=['zone_id', 'zone']),
        engine=dict(type='str', choices=["MySQL", "SQLServer", "PostgreSQL", "PPAS"]),
        engine_version=dict(type='str'),
        instance_net_type=dict(type='str', choices=["Internet", "Intranet"], aliases=['db_instance_net_type']),
        description=dict(type='str', aliases=['db_instance_description']),
        security_ips=dict(type='str'),
        instance_charge_type=dict(type='str', choices=["Postpaid", "Prepaid"]),
        period=dict(type='int', choices=range(1, 10).extend([12, 24, 36])),
        connection_mode=dict(type='str', choices=["Performance", "Safty"]),
        vpc_id=dict(type='str'),
        vswitch_id=dict(type='str'),
        private_ip_address=dict(type='str'),
        instance_id=dict(type='str', aliases=['db_instance_id']),
        tags=dict(type='str', aliases=['instance_tags']),
        page_size=dict(type='int', default=30, choices=[30, 50, 100]),
        page_number=dict(type='int', default=1),
        auto_renew_period=dict(type='int', choices=[1, 2, 3, 6, 12]),
        auto_renew=dict(type='bool'),
        public_connection_string_prefix=dict(type='str'),
        private_connection_string_prefix=dict(type='str'),
        dest_connection_string_prefix=dict(type='str'),
        dest_port=dict(type='str'),
        public_port=dict(type='str'),
        private_port=dict(type='int', choices=range(3001, 4000)),
        current_connection_string=dict(type='str'),
        instance_type=dict(type='str', aliases=['db_instance_class']),
        instance_storage=dict(type='int', aliases=['db_instance_storage'])
    ))
    modules = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        modules.fail_json(msg="Package 'footmark' required for the module alicloud_rds_instance.")

    rds = rds_connect(modules)
    vpc = vpc_connect(modules)

    state = modules.params['state']
    alicloud_zone = modules.params['alicloud_zone']
    engine = modules.params['engine']
    engine_version = modules.params['engine_version']
    instance_net_type = modules.params['instance_net_type']
    description = modules.params['description']
    security_ips = modules.params['security_ips']
    instance_charge_type = modules.params['instance_charge_type']
    period = modules.params['period']
    connection_mode = modules.params['connection_mode']
    vswitch_id = modules.params['vswitch_id']
    private_ip_address = modules.params['private_ip_address']
    instance_id = modules.params['instance_id']
    tags = modules.params['tags']
    page_size = modules.params['page_size']
    page_number = modules.params['page_number']
    auto_renew_period = modules.params['auto_renew_period']
    auto_renew = modules.params['auto_renew']
    public_connection_string_prefix = modules.params['public_connection_string_prefix']
    private_connection_string_prefix = modules.params['private_connection_string_prefix']
    public_port = modules.params['public_port']
    private_port = modules.params['private_port']
    current_connection_string = modules.params['current_connection_string']
    dest_connection_string_prefix = modules.params['dest_connection_string_prefix']
    dest_port = modules.params['dest_port']
    instance_type = modules.params['instance_type']
    instance_storage = modules.params['instance_storage']

    vpc_id = None
    instance_network_type = 'Classic'
    current_instance = None
    changed = False
    if vswitch_id:
        instance_network_type = 'VPC'
        try:
            vswitch_obj = vpc.get_vswitch_attribute(vswitch_id)
            if vswitch_obj:
                vpc_id = vswitch_obj.vpc_id
        except Exception as e:
            modules.fail_json(msg=str("Unable to get vswitch, error:{0}".format(e)))
    if instance_id:
        try:
            current_instance = rds.describe_db_instance_attribute(instance_id)
        except Exception as e:
            modules.fail_json(msg=str("Unable to describe instance, error:{0}".format(e)))

    if state == 'absent':
        if current_instance:
            if current_connection_string:
                try:
                    changed = current_instance.release_public_connection_string(current_connection_string)
                    modules.exit_json(changed=changed, instance=get_info(current_instance))
                except Exception as e:
                    modules.fail_json(msg=str("Unable to release public connection string error: {0}".format(e)))
            try:
                changed = current_instance.terminate()
                modules.exit_json(changed=changed, instance=get_info(current_instance))
            except Exception as e:
                modules.fail_json(msg=str("Unable to release instance error: {0}".format(e)))
        modules.fail_json(msg=str("Unable to operate your instance, please check your instance_id and try again!"))
    if state == 'restart':
        if current_instance:
            try:
                changed = current_instance.restart()
                modules.exit_json(changed=changed, instance=get_info(current_instance))
            except Exception as e:
                modules.fail_json(msg=str("Unable to restart instance error: {0}".format(e)))
        modules.fail_json(msg=str("Unable to restart your instance, please check your instance_id and try again!"))
    if not current_instance:
        try:
            client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
            current_instance = rds.create_rds_instance(engine=engine,
                                                       engine_version=engine_version,
                                                       db_instance_class=instance_type,
                                                       db_instance_storage=instance_storage,
                                                       db_instance_net_type=instance_net_type,
                                                       security_ip_list=security_ips,
                                                       pay_type=instance_charge_type,
                                                       client_token=client_token,
                                                       instance_network_type=instance_network_type,
                                                       period='Month',
                                                       used_time=period,
                                                       alicloud_zone=alicloud_zone,
                                                       db_instance_description=description,
                                                       connection_mode=connection_mode,
                                                       vpc_id=vpc_id,
                                                       vswitch_id=vswitch_id,
                                                       private_ip_address=private_ip_address)
            instance_id = current_instance.dbinstance_id
        except Exception as e:
            modules.fail_json(msg=str("Unable to create rds instance error: {0}".format(e)))
    if auto_renew:
        try:
            changed = current_instance.modify_auto_renewal_attribute(duration=auto_renew_period, auto_renew=auto_renew)
        except Exception as e:
            modules.fail_json(msg=str("Unable to modify rds instance auto renewal attribute error: {0}".format(e)))
    if public_connection_string_prefix and public_port:
        try:
            changed = current_instance.allocate_public_connection_string(public_connection_string_prefix, public_port)
        except Exception as e:
            modules.fail_json(msg=str("Unable to allocate public connection error: {0}".format(e)))
    if private_connection_string_prefix:
        try:
            changed = current_instance.allocate_private_connection_string(private_connection_string_prefix, private_port)
        except Exception as e:
            modules.fail_json(msg=str("Unable to allocate private connection string error: {0}".format(e)))
    if current_connection_string:
        try:
            changed = current_instance.modify_connection_string(current_connection_string, dest_connection_string_prefix, dest_port)
        except Exception as e:
            modules.fail_json(msg=str("Unable to modify current connection string error: {0}".format(e)))
    # get newest instance
    try:
        current_instance = rds.describe_db_instance_attribute(instance_id)
    except Exception as e:
        modules.fail_json(msg=str("Unable to describe instance error: {0}".format(e)))
    modules.exit_json(changed=changed, instance=get_info(current_instance))


if __name__ == '__main__':
    main()


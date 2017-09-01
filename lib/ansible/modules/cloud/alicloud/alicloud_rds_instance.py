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
version_added: "2.4"
short_description: Create, Start, Stop, Restart or Terminate an Instance in RDS.
description:
    - Create, start, stop, restart, modify or terminate rds instances.
options:
  state:
    description:
      - The state of the instance after operating.
    default: 'present'
    choices: [ 'present', 'restart', 'absent' ]
  alicloud_zone:
    description:
      - Aliyun availability zone ID in which to launch the instance.
        If it is not specified, it will be allocated by system automatically.
    aliases: ['acs_zone', 'ecs_zone', 'zone_id', 'zone' ]
  engine:
    description: Database type. Required when C(state=present).
    choices: [ 'MySQL', 'SQLServer', 'PostgreSQL', 'PPAS' ]
  engine_version:
    description:
      - The database version number, as follows:
        MySQL: 5.5 / 5.6 / 5.7;
        SQLServer: 2008r2 / 2012;
        PostgreSQL: 9.4;
        PPAS: 9.3.
        Required when C(state=present).
  db_instance_class:
    description: Instance specification. Required when C(state=present).
  db_instance_storage:
    description:
      - Customize storage, range:
        MySQL / PostgreSQL / PPAS dual high-availability version of [5,2000];
        MySQL 5.7 standalone basic version is [20,1000];
        SQL Server 2008R2 is [10,2000];
        SQL Server 2012 standalone basic version of [20,2000];
        Increased every 5G. Unit: GB.
        Required when C(state=present).
  db_instance_net_type:
    description:
      - Instance of the network connection type: Internet on behalf of the public network, Intranet on behalf of the private network.
        Required when C(state=present).
    choices: ["Internet", "Intranet"]
  db_instance_description:
    description:
      - Instance description or memo information, no more than 256 bytes;
        Note: You can not start with http: //, https: //. Start with Chinese and English letters.
        Can contain Chinese, English characters, "_", "-", the number of characters length 2 ~ 256.
  security_ip_list:
    description:
      - Allow access to the IP list of all databases under this instance,
        separated by commas, not repeatable, up to 1000;
        Supported formats:%, 0.0.0.0/0,10.23.12.24 (IP),
        or 10.23.12.24/24 (CIDR mode , No class interdomain routing,
        / 24 indicates the length of the prefix in the address,
        the range [1,32]) where 0.0.0.0 / 0, that does not limit
        Required when C(state=present).
  pay_type:
    description:
      - Type of payment. Postpaid: postpaid instance; Prepaid: prepaid instance. Required when C(state=present).
    choices: [ "Postpaid", "Prepaid" ]
  period:
    description:
      - If the payment type is Prepaid, the entry must be passed in. Specify the prepaid instance as the year of the year or month.
        Required when C(pay_type="PrePaid").
    choices: ["Year", "Month"]
  used_time:
    description:
      - If the payment type is Prepaid, the entry must be passed in. Specify the purchase time, according to the need to pass 1, 2, 3 and other values.
  client_token:
    description: Used to ensure idempotency. Required when C(state=present).
  instance_network_type:
    description:
      - VPC: create VPC instance; Classic: create Classic instance; do not fill, the default creation of Classic instance.
    default: Classic
    choices: ["VPC", "Classic"]
  connection_mode:
    description:
      - Performance is standard access mode; Safty is a high security access mode; default is RDS system allocation.
    choices: ["Performance", "Safty"]
  vpc_id:
    description:
      - VPC id
  vswitch_id:
    description:
      - Vswitch id
  private_ip_address:
    description: Users can specify VSvitchId under vpcIp, if not input, the system automatically assigned.
  db_instance_id:
    description:
      - Whether allocate a public ip for the new instance. Required when C(state in ["present", "absent", "restart"])
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
  duration:
    description:
      - Automatic renewal period. Required when C(auto_renew='True')
    choices: [1~12]
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
    - "python >= 2.7"
    - "footmark"
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
        db_instance_class: rds.mysql.t1.small
        db_instance_storage: 30
        db_instance_net_type: Internet
        security_ip_list: 10.23.12.24/24
        pay_type: Postpaid

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
        db_instance_id: rm-2ze3083kmle92v50t
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
        db_instance_id: rm-2ze3083kmle92v50t

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
        db_instance_id: rm-2ze3083kmle92v50t

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
        db_instance_id: rm-2ze3083kmle92v50t

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
        db_instance_id: rm-2ze3083kmle92v50t

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
        db_instance_id: rm-2ze3083kmle92v50t

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
        db_instance_id: rm-2ze3083kmle92v50t
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
      "engine": "MySQL",
      "engine_version": "5.6",
      "instance_network_type": "Classic"
  }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, rds_connect

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
                engine=obj.engine,
                engine_version=obj.engine_version,
                instance_network_type=obj.instance_network_type,
                connection_string=obj.connection_string)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default="present", choices=["present", "absent", "restart"], alias=['status']),
        alicloud_zone=dict(type='str', aliases=['acs_zone', 'ecs_zone', 'zone_id', 'zone']),
        engine=dict(type='str', choices=["MySQL", "SQLServer", "PostgreSQL", "PPAS"]),
        engine_version=dict(type='str'),
        db_instance_net_type=dict(type='str', choices=["Internet", "Intranet"]),
        db_instance_description=dict(type='str'),
        security_ip_list=dict(type='str'),
        pay_type=dict(type='str', choices=["Postpaid", "Prepaid"]),
        period=dict(type='str', choices=["Month", "Year"]),
        used_time=dict(type='str'),
        client_token=dict(type='str'),
        instance_network_type=dict(type='str', choices=["VPC", "Classic"], default="Classic"),
        connection_mode=dict(type='str', choices=["Performance", "Safty"]),
        vpc_id=dict(type='str'),
        vswitch_id=dict(type='str'),
        private_ip_address=dict(type='str'),
        db_instance_id=dict(type='str'),
        tags=dict(type='str', aliases=['instance_tags']),
        page_size=dict(type='int', default=30, choices=[30, 50, 100]),
        page_number=dict(type='int', default=1),
        duration=dict(type='int', choices=range(1, 13)),
        auto_renew=dict(type='bool'),
        public_connection_string_prefix=dict(type='str'),
        private_connection_string_prefix=dict(type='str'),
        dest_connection_string_prefix=dict(type='str'),
        dest_port=dict(type='str'),
        public_port=dict(type='str'),
        private_port=dict(type='int', choices=range(3001, 4000)),
        current_connection_string=dict(type='str'),
        db_instance_class=dict(type='str'),
        db_instance_storage=dict(type='int')
    ))
    modules = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_rds_instance.")

    rds = rds_connect(modules)

    state = modules.params['state']
    alicloud_zone = modules.params['alicloud_zone']
    engine = modules.params['engine']
    engine_version = modules.params['engine_version']
    db_instance_net_type = modules.params['db_instance_net_type']
    db_instance_description = modules.params['db_instance_description']
    security_ip_list = modules.params['security_ip_list']
    pay_type = modules.params['pay_type']
    period = modules.params['period']
    used_time = modules.params['used_time']
    client_token = modules.params['client_token']
    instance_network_type = modules.params['instance_network_type']
    connection_mode = modules.params['connection_mode']
    vpc_id = modules.params['vpc_id']
    vswitch_id = modules.params['vswitch_id']
    private_ip_address = modules.params['private_ip_address']
    db_instance_id = modules.params['db_instance_id']
    tags = modules.params['tags']
    page_size = modules.params['page_size']
    page_number = modules.params['page_number']
    duration = modules.params['duration']
    auto_renew = modules.params['auto_renew']
    public_connection_string_prefix = modules.params['public_connection_string_prefix']
    private_connection_string_prefix = modules.params['private_connection_string_prefix']
    public_port = modules.params['public_port']
    private_port = modules.params['private_port']
    current_connection_string = modules.params['current_connection_string']
    dest_connection_string_prefix = modules.params['dest_connection_string_prefix']
    dest_port = modules.params['dest_port']
    db_instance_class = modules.params['db_instance_class']
    db_instance_storage = modules.params['db_instance_storage']

    current_instance = None
    changed = False

    if db_instance_id:
        try:
            current_instance = rds.describe_db_instance_attribute(db_instance_id)
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
                changed = current_instance.release()
                modules.exit_json(changed=changed, instance=get_info(current_instance))
            except Exception as e:
                modules.fail_json(msg=str("Unable to release instance error: {0}".format(e)))
    if state == 'restart':
        try:
            changed = current_instance.restart()
            modules.exit_json(changed=changed, instance=get_info(current_instance))
        except Exception as e:
            modules.fail_json(msg=str("Unable to restart instance error: {0}".format(e)))
    if not current_instance:
        try:
            current_instance = rds.create_rds_instance(engine=engine,
                                                       engine_version=engine_version,
                                                       db_instance_class=db_instance_class,
                                                       db_instance_storage=db_instance_storage,
                                                       db_instance_net_type=db_instance_net_type,
                                                       security_ip_list=security_ip_list,
                                                       pay_type=pay_type,
                                                       client_token=client_token,
                                                       period=period,
                                                       alicloud_zone=alicloud_zone,
                                                       db_instance_description=db_instance_description,
                                                       used_time=used_time,
                                                       instance_network_type=instance_network_type,
                                                       connection_mode=connection_mode,
                                                       vpc_id=vpc_id,
                                                       vswitch_id=vswitch_id,
                                                       private_ip_address=private_ip_address)
            db_instance_id = current_instance.dbinstance_id
        except Exception as e:
            modules.fail_json(msg=str("Unable to create rds instance error: {0}".format(e)))
    if auto_renew:
        try:
            changed = current_instance.modify_auto_renewal_attribute(duration=duration, auto_renew=auto_renew)
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
        current_instance = rds.describe_db_instance_attribute(db_instance_id)
    except Exception as e:
        modules.fail_json(msg=str("Unable to describe instance error: {0}".format(e)))
    modules.exit_json(changed=changed, instance=get_info(current_instance))


if __name__ == '__main__':
    main()


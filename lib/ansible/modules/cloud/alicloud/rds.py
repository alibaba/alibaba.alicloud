#!/usr/bin/python
#
# Copyright 2017 Alibaba Group Holding Limited.
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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}

DOCUMENTATION = """
---
module: rds
short_description: Create instance, Create database, Create read-only instance, Modify rds instance,
                   Change rds instance type, Restart instance, Switch between primary and standby database,
                   Delete database and Release Instance in RDS.
description:
     - Create instance, Create database, Create read-only instance, Modify rds instance, Change rds instance type,
      Restart instance, Switch between primary and standby database, Delete database and Release Instance in RDS.
common options:
  alicloud_access_key:
    description:
      - Aliyun Cloud access key. If not set then the value of the `ALICLOUD_ACCESS_KEY`, `ACS_ACCESS_KEY_ID`, 
        `ACS_ACCESS_KEY` or `ECS_ACCESS_KEY` environment variable is used.
    required: false
    default: null
    aliases: ['acs_access_key', 'ecs_access_key','access_key']
  alicloud_secret_key:
    description:
      - Aliyun Cloud secret key. If not set then the value of the `ALICLOUD_SECRET_KEY`, `ACS_SECRET_ACCESS_KEY`,
        `ACS_SECRET_KEY`, or `ECS_SECRET_KEY` environment variable is used.
    required: false
    default: null
    aliases: ['acs_secret_access_key', 'ecs_secret_key','secret_key']
  command:
    description:
      -  command for rds,
    choices: [ 'create', 'delete', 'replicate', 'modify', 'reboot', 'switch' ]
    required: True
    default: create

function: create rds instances
  description: create rds instances.
  command: create
  options:    
    alicloud_region:
      description:
        - The Aliyun Cloud region to use. If not specified then the value of the `ALICLOUD_REGION`, `ACS_REGION`, 
          `ACS_DEFAULT_REGION` or `ECS_REGION` environment variable, if any, is used.
      required: false
      default: null
      aliases: ['acs_region', 'ecs_region', 'region']
    alicloud_zone:
      description:
        - availability zone in which to launch the instance. Used only when command=create, command=replicate.
      required: false
      default: null
      aliases: ['acs_zone', 'ecs_zone']
    db_engine:
      description:
        - The type of database.
      required: true
      default: null
      choices: [ 'MySQL','SQLServer', 'PostgreSQL', 'PPAS']
    engine_version:
      description:
        - Version number of the database engine to use. If not specified, then the current Aliyun RDS default engine
        version is used.
      required: false
      default: null
    db_instance_class:
      description:
        - The instance type of the database.  Must be specified when command=create. Optional when command=replicate,
        command=modify. If not specified then the replica inherits the same instance type as the source instance.
      required: true
      default: null
      aliases: ['instance_type']
    db_instance_storage:
      description:
        - Size in gigabytes of the initial storage for the DB instance.
      required: true
      default: null
      aliases: ['size']
    instance_net_type:
      description:
        - The net type of the DB instance
      required: true
      default: false
      choices: ['Internet', 'Intranet']
    instance_description:
      description:
        - The description of the DB instance
      required: false
      default: null
    security_ip_list:
      description:
        - IP list that be allowed to access all DBs in the instance. Support CIDR mode.
      required: true
      default: null
    pay_type:
      description:
        - The pay type of the DB instance.
      required: true
      default: null
      choices: ['Postpaid', 'Prepaid']
    period:
      description:
        - The type of the "Prepaid"
      default: null
      required: (depends on pay_type)
      choices: ['Year', 'Month']
    used_time:
      description:
        - The duration of the "Prepaid"
      default: null
      required: (depends on pay_type)
      choices: (depends on period)
    instance_network_type:
      description:
        - The network type of the instance.
      default: Classic
      required: false
      choices: ['VPC', 'Classic']
      aliases: ['network_type']
    connection_mode:
      description:
        - The connection mode of the rds instance.      
      required: false
      choices: ['Performance', 'Safe']      
    vpc_id:
      description:
        - The ID of the VPC.
      default: null
      required: (depends on network_type)
    vswitch_id:
      description:
        - The ID of the VSwitch.
      default: null
      required: (depends on network_type)
    private_ip_address:
      description:
        - IP address of an VPC under VSwitchId. If no value is specified, the system will automatically assign a VPC
        IP address.
      default: null
      required: false
    allocate_public_ip :
      description:
        - Whether to allocate public IP.
      default: null
      required: false
    connection_string_prefix:
      description:
        - The public connection string.
      default: null
      required: false
    public_port:
      description:
        - The public connection port.
      default: null
      required: false
    db_name:
      description:
        - Name of a database to create within the instance.  If not specified then no database is created.
      required: false
      default: null
    db_description:
      description:
        - Description of a database to create within the instance. 
      required: false
      default: null
    character_set_name:
      description:
        - Associate the DB instance with a specified character set.
      required: false
      default: null
    maint_window:
      description:
        - "Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.  (Example: Mon:22:00-Mon:23:15) If not specified
        then a random maintenance window is assigned."
      required: false
      default: null
    preferred_backup_time:
      description:
        - Backup time, in the format ofHH:mmZ- HH:mm Z.This parameter is required if preferred_backup_period and
         backup_retention_period is passed.
      required: false
      default: null      
    preferred_backup_period:
      description:
        - Backup period.
      required: false
      default: null
      aliases: ['backup_window']
    backup_retention_period:
      description:
        - "Number of days backups are retained.  Set to 0 to disable backups.  Default is 7 day.  Valid range: 7-730.
      required: false
      default: null
      aliases: ['backup_retention']
    db_tags:
      description:
        - A hash/dictionaries of db tags, '{"tag_key": "tag_value"}', tag_key must be not null when tag_value isn't null.
      required: false
      default: null
    wait:
      description:
        - wait for the RDS instance to be in state 'running' before returning.
      required: false
      default: "no"
      choices: [ "yes", "no" ]
    wait_timeout:
      description:
        - how long before wait gives up, in seconds
      required: false
      default: 300

function: change rds instance type
  description: change rds instance type
  command: modify
  options:
    instance_id:
      description:
        - ID of the database to change.
      required: true
      default: null      
    alicloud_region:
      description:
        - The ACS region to use. If not specified then the value of the ECS_REGION environment variable,
        if any, is used.
      required: false
      aliases: [ 'acs_region', 'ecs_region' ]
    db_instance_class:
      description:
        - The instance type of the database.  Must be specified when command=create. Optional when command=replicate,
        command=modify. If not specified then the replica inherits the same instance type as the source instance.
      required: false
      default: null
      aliases: ['instance_type']
    db_instance_storage:
      description:
        - Size in gigabytes of the initial storage for the DB instance.
      required: false
      default: null
      aliases: ['size']
    pay_type:
      description:
        - The pay type of the DB instance.
      required: true
      default: null
      choices: ['Postpaid']

function: create an rds read-only instance
  description: create a read-only replica of an existing instance.
  command: replicate
  options:
    source_instance:
      description:
        - ID of the database to replicate.
      required: true
      default: null
      aliases: ['instance_id']
    alicloud_region:
      description:
        - The ACS region to use. If not specified then the value of the ECS_REGION environment variable,
        if any, is used.
      required: true
      aliases: [ 'acs_region', 'ecs_region' ]
    alicloud_zone:
      description:
        - availability zone in which to launch the instance. Used only when command=create, command=replicate.
      required: true
      default: null
      aliases: ['acs_zone', 'ecs_zone']
    engine_version:
      description:
        - Version number of the database engine to use. If not specified, then the current Aliyun RDS default engine
         version is used.
      required: true
      default: null
    db_instance_class:
      description:
        - The instance type of the database.  Must be specified when command=create. Optional when command=replicate,
        command=modify. If not specified then the replica inherits the same instance type as the source instance.
      required: true
      default: null
      aliases: ['instance_type']
    db_instance_storage:
      description:
        - Size in gigabytes of the initial storage for the DB instance.
      required: true
      default: null
      aliases: ['size']
    pay_type:
      description:
        - The pay type of the DB instance.
      required: true
      default: null
      choices: ['Postpaid']
    instance_description:
      description:
        - The description of the DB instance
      required: false
      default: null
    instance_network_type:
      description:
        - The network type of the instance.
      default: Classic
      reqired: false
      choices: ['VPC', 'Classic']
      aliases: ['network_type']
    vpc_id:
      description:
        - The ID of the VPC.
      default: null
      required: False
    vswitch_id:
      description:
        - The ID of the VSwitch.
      default: null
      required: False
    private_ip_address:
      description:
        - IP address of an VPC under VSwitchId. If no value is specified, the system will automatically assign a VPC
        IP address.
      default: null
      required: false

function: modify rds instances
  description: modify rds instances.
  command: modify
  options:    
    alicloud_region:
      description:
        - The Aliyun Cloud region to use. If not specified then the value of the `ALICLOUD_REGION`, `ACS_REGION`, 
          `ACS_DEFAULT_REGION` or `ECS_REGION` environment variable, if any, is used.
      required: false
      default: null
      aliases: ['acs_region', 'ecs_region', 'region']
    instance_id:
      description:
        - ID of the database to change.
      required: true
      default: null    
    current_connection_string:
      description:
        - Current connection string of an instance.
      default: null
      required: false
    connection_string_ prefix:
      description:
        - Target connection string.
      default: null
      required: false
    port:
      description:
        - Target port.
      default: null
      required: false
    connection_mode:
      description:
        - The connection mode of the rds instance.      
      reqired: false
      choices: ['Performance', 'Safe'] 
    db_instance_class:
      description:
        - The instance type of the database.  Must be specified when command=create. Optional when command=replicate,
        command=modify. If not specified then the replica inherits the same instance type as the source instance.
      required: false
      default: null
      aliases: ['instance_type']  
    db_instance_storage:
      description:
        - Size in gigabytes of the initial storage for the DB instance.
      required: true
      default: null
      aliases: ['size']   
    pay_type:
      description:
        - The pay type of the DB instance.
      required: true
      default: null
      choices: ['Postpaid'] 
    instance_description:
      description:
        - The description of the DB instance
      required: false
      default: null      
    security_ip_list:
      description:
        - IP list that be allowed to access all DBs in the instance. Support CIDR mode.
      required: true
      default: null
    instance_network_type:
      description:
        - The network type of the instance.
      default: Classic
      reqired: false
      choices: ['VPC', 'Classic']
      aliases: ['network_type']
    vpc_id:
      description:
        - The ID of the VPC.
      default: null
      required: (depends on network_type)
    vswitch_id:
      description:
        - The ID of the VSwitch.
      default: null
      required: (depends on network_type)
    maint_window:
      description:
        - "Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.  (Example: Mon:22:00-Mon:23:15) If not specified
        then a random maintenance window is assigned."
      required: false
      default: null
    preferred_backup_time:
      description:
        - Backup time, in the format ofHH:mmZ- HH:mm Z.This parameter is required if preferred_backup_period and
        backup_retention_period is passed.
      required: false
      default: null      
    preferred_backup_period:
      description:
        - Backup period.
      required: false
      default: null
      aliases: ['backup_window']
    backup_retention_period:
      description:
        - "Number of days backups are retained. Default is 7 day.  Valid range: 7-730.
      required: false
      default: null
      aliases: ['backup_retention']

function: create a database
    description: Creates a new database in an instance
    command: create
    options:
      instance_id:
        description:
          - Id of instance.
        required: True
      db_name:
        description:
          - Name of a database to create within the instance.  If not specified, then no database is created
        required: True
      db_description:
        description:
          - Description of a database to create within the instance. 
        required: False
      character_set_name:
        description:
          - Associate the DB instance with a specified character set
        required: True


function: delete a database
    description: Users can delete databases from instances to do this
    command: delete
    options:
      instance_id:
        description:
          - Id of instance.
        required: True
      db_name:
        description:
          - Name of a database to delete within the instance. If not specified, then no database is deleted
        required: True


function: switch between primary and standby database of an rds instance
    description: user can switch between primary and standby database of rds instance
    command: switch
    options:
      instance_id:
        description:
          - Id of instances to modify
        required: True
      node_id:
        description:
          - Unique ID of a node
        required: True
      force:
        default: No
        choices: ['Yes', 'No']
        required: False


function: Restart an rds instance
    description: Generally, an RDS instance can be restarted within 10s. If a large number of transactions must be
    submitted or rolled back, the restart may be extended by about one minute
    command: reboot
    options:
      instance_id:
        description:
          - Id of instances to reboot
        required: True


function: Release an rds instance
    description: Releases an RDS instance
    command: delete
    options:
      instance_id:
        description:
          - Id of instances to remove
        required: True


"""

EXAMPLES = """
#
# provisioning for rds
#


# basic provisioning example to create rds instance

- name: create rds instance
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    command: create
    alicloud_zone: cn-beijing-a
    db_engine: MySQL 
    engine_version: 5.6
    db_instance_class: rds.mysql.t1.small
    db_instance_storage: 10 
    instance_net_type: Intranet
    instance_description: ahttp://
    security_ip_list: 192.168.0.2/24
    pay_type: Postpaid
    connection_mode: Safe
    instance_network_type: VPC
    vpc_id: xxxxxxxxxx	
    vswitch_id: xxxxxxxxxx
    private_ip_address: 192.168.0.25
    allocate_public_ip: yes
    connection_string_prefix: test
    public_port: 3306
    db_name: testmysql
    db_description: test mysql 
    character_set_name: utf8
    maint_window: 02:00Z-06:00Z
    preferred_backup_time: 02:00Z-03:00Z
    preferred_backup_period: Monday,Tuesday
    backup_retention_period: 7
    wait: yes
    wait_timeout: 20
    db_tags:	
      name: test
  tasks:
    - name: create rds instance
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        command: '{{ command }}'
        db_engine: '{{ db_engine }}'
        engine_version: '{{ engine_version }}'
        db_instance_class: '{{ db_instance_class }}'
        db_instance_storage: '{{ db_instance_storage }}'		
        instance_net_type: '{{ instance_net_type }}'
        instance_description: '{{ instance_description }}'
        security_ip_list: '{{ security_ip_list }}'
        pay_type: '{{ pay_type }}'  
        connection_mode: '{{ connection_mode }}'
        instance_network_type: '{{ instance_network_type }}'
        vpc_id: '{{ vpc_id }}'
        vswitch_id: '{{ vswitch_id }}'
        private_ip_address: '{{ private_ip_address }}'
        allocate_public_ip: '{{ allocate_public_ip }}'
        connection_string_prefix: '{{ connection_string_prefix }}'
        public_port: '{{ public_port }}'
        db_name: '{{ db_name }}'    
        db_description: '{{ db_description }}'
        character_set_name: '{{ character_set_name }}'
        maint_window: '{{ maint_window }}'
        preferred_backup_time: '{{ preferred_backup_time }}'
        preferred_backup_period: '{{ preferred_backup_period }}'
        backup_retention_period: '{{ backup_retention_period }}'
        db_tags: '{{ db_tags }}'
        wait: '{{ wait }}'
        wait_timeout: '{{ wait_timeout }}'
      register: result
    - debug: var=result

# basic provisioning example to change rds instance type

- name: change rds instance type
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    command: modify
    instance_id: xxxxxxxxxx
    db_instance_class: rds.mysql.s1.small
    db_instance_storage: 35 
    pay_type: Postpaid
  tasks:
    - name: change rds instance type
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
        db_instance_class: '{{ db_instance_class }}'
        db_instance_storage: '{{ db_instance_storage }}'
        pay_type: '{{ pay_type }}'
      register: result
    - debug: var=result   

# basic provisioning example to modify rds instance   
 
- name: modify rds instance
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    command: modify
    instance_id: xxxxxxxxxx
    db_instance_class: rds.mysql.t1.small
    db_instance_storage: 45    
    instance_description: xyz 
    security_ip_list: 192.168.0.2/24
    pay_type: Postpaid
    connection_mode: Safe
    instance_network_type: VPC
    vpc_id: xxxxxxxxxx	
    vswitch_id: xxxxxxxxxx
    current_connection_string: test.mysql.rds.aliyuncs.com
    connection_string_prefix: test123
    port: 3390
    maint_window: 02:00Z-06:00Z
    preferred_backup_time:  02:00Z-03:00Z
    preferred_backup_period: Monday
    backup_retention_period: 50
  tasks:
    - name: modify rds instance
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
        db_instance_class: '{{ db_instance_class }}'
        db_instance_storage: '{{ db_instance_storage }}'		
        instance_description: '{{ instance_description }}'
        security_ip_list: '{{ security_ip_list }}'
        pay_type: '{{ pay_type }}'      
        connection_mode: '{{ connection_mode }}'
        instance_network_type: '{{ instance_network_type }}'
        vpc_id: '{{ vpc_id }}'
        vswitch_id: '{{ vswitch_id }}'
        current_connection_string: '{{ current_connection_string }}'
        connection_string_prefix: '{{ connection_string_prefix }}'
        port: '{{ port }}'
        maint_window: '{{ maint_window }}'
        preferred_backup_time: '{{ preferred_backup_time }}'
        preferred_backup_period: '{{ preferred_backup_period }}'
        backup_retention_period: '{{ backup_retention_period }}'
      register: result
    - debug: var=result 

# basic provisioning example to create database

- name: create database
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hongkong
    command: create
    instance_id: xxxxxxxxxx
    db_name: testdb
    db_description: test
    character_set_name: utf8
  tasks:
    - name: create database
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
        db_name: '{{ db_name }}'
        db_description: '{{ db_description }}'
        character_set_name: '{{ character_set_name }}'
      register: result
    - debug: var=result
    
# basic provisioning example to delete database

- name: delete database
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hongkong
    command: delete
    instance_id: xxxxxxxxxx
    db_name: testdb
  tasks:
    - name: delete database
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
        db_name: '{{ db_name }}'
      register: result
    - debug: var=result
    
# basic provisioning example to switch between primary and standby database of an rds

- name: switch between primary and standby database
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-hongkong
    command: switch
    instance_id: xxxxxxxxxx
    node_id: xxxxxxxxxx
    force: 'Yes'
  tasks:
    - name: switch between primary and standby database
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
        node_id: '{{ node_id }}'
        force: '{{ force }}'
      register: result
    - debug: var=result
    
# basic provisioning example to restart rds instance

- name: Restart RDS Instance
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    command: reboot
    instance_id: xxxxxxxxxx
  tasks:
    - name: Restart RDS Instance
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
      register: result
    - debug: var=result
    
# basic provisioning example to release rds instance

- name: Release RDS Instance
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    command: delete
    instance_id: xxxxxxxxxx
  tasks:
    - name: Release RDS Instance
      rds:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        command: '{{ command }}'
        instance_id: '{{ instance_id }}'
      register: result
    - debug: var=result

"""


import time
from ast import literal_eval
from footmark.exception import RDSResponseError


def create_rds_instance(module, rds, zone, db_engine, engine_version, db_instance_class, db_instance_storage,
                        instance_net_type, instance_description, security_ip_list, pay_type, period, used_time,
                        instance_network_type, connection_mode, vpc_id, vswitch_id, private_ip_address,
                        allocate_public_ip, connection_string_prefix, public_port, db_name, db_description,
                        character_set_name, maint_window, preferred_backup_time,
                        preferred_backup_period, backup_retention_period, db_tags, wait, wait_timeout):
    """
    Create RDS Instance

    :param module:  Ansible module object
    :param rds:  Authenticated rds connection object
    :param zone:  ID of a zone to which an instance belongs
    :param db_engine: The type of database
    :param engine_version: Version number of the database engine to use
    :param db_instance_class: The instance type of the database.
    :param db_instance_storage: Size in gigabytes of the initial storage for the DB instance.
    :param instance_net_type: The net type of the DB instance
    :param instance_description: Instance description or remarks, no more than 256 bytes.
    :param security_ip_list: List of IP addresses allowed to access all databases of an instance.
    :param pay_type: The pay type of the DB instance.
    :param period: Period of the instance if pay_type set to prepaid.
    :param used_time: This parameter specifies the duration for purchase.
    :param instance_network_type: The network type of the instance.
    :param connection_mode: The connection mode of the instance
    :param vpc_id: The ID of the VPC
    :param vswitch_id: ID of VSwitch
    :param private_ip_address: IP address of an VPC under VSwitchId.
    :param allocate_public_ip: Whether to allocate public IP
    :param connection_string_prefix: Prefix of an Internet connection string
    :param public_port: The public connection port.
    :param db_name: Name of a database to create within the instance.
    :param db_description: Description of a database to create within the instance.
    :param character_set_name: Associate the DB instance with a specified character set.
    :param maint_window: Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.
    :param preferred_backup_time: Backup time, in the format of HH:mmZ- HH:mm Z.
    :param preferred_backup_period: Backup period.
    :param backup_retention_period: Retention days of the backup
    :param db_tags: A list of hash/dictionaries of db tags
    :param wait: Wait for the RDS instance to be 'running' before returning.
    :param wait_timeout: how long before wait gives up, in seconds
    :return:
        changed: If instance is created successfully the changed will be set
            to True else False
        DBInstanceId: the newly created instance id
    """

    changed = False
    result = []
    if not db_engine:
        module.fail_json(msg='db_engine is required to create rds instance')
    if not db_instance_class:
        module.fail_json(msg='db_instance_class is required to create rds instance')
    if not db_instance_storage:
        module.fail_json(msg='db_instance_storage is required to create rds instance')
    if not instance_net_type:
        module.fail_json(msg='instance_net_type is required to create rds instance')
    if not security_ip_list:
        module.fail_json(msg='security_ip_list is required to create rds instance')
    if not pay_type:
        module.fail_json(msg='pay_type is required to create rds instance')
    if str(pay_type) == "Prepaid":
        if not period:
            module.fail_json(msg='period is required to create rds instance')
        if not used_time:
            module.fail_json(msg='used_time is required to create rds instance')

    if allocate_public_ip:
        if not connection_string_prefix:
            module.fail_json(msg='connection_string_prefix is required set public connection')
        if public_port:
            if str(public_port).isdigit():
                if int(public_port) < 3200 or int(public_port) > 3999:
                    module.fail_json(msg='public_port is limited to [3200-3999]')
            else:
                module.fail_json(msg='The public_port must be an integer value, entered value is {0}'.format(
                    public_port))
        else:     
            module.fail_json(msg='public_port is required set public connection')
    if db_instance_storage:
        if str(db_instance_storage).isdigit():
            if int(db_instance_storage) < 5 or int(db_instance_storage) > 2000:
                module.fail_json(msg='db_instance_storage is limited to [5-2000]')
            if int(db_instance_storage) % 5 != 0:
                module.fail_json(msg='db_instance_storage must be multiple of 5GB')
        else:
            module.fail_json(msg='The db_instance_storage must be an integer value, entered value is {0}'.format(
                db_instance_storage))

    if db_name:
        if len(db_name) > 64:
            module.fail_json(msg='db_name is limited to maximum of 64 character')

    if backup_retention_period:
        if str(backup_retention_period).isdigit():
            if int(backup_retention_period) < 7 or int(backup_retention_period) > 730:
                module.fail_json(msg='backup_retention_period is limited to [7-730]')
        else:
            module.fail_json(msg='The backup_retention_period must be an integer value, entered value is {0}'.format(
                backup_retention_period))
    if instance_description:
        if instance_description.startswith('http://') or instance_description.startswith('https://'):
            module.fail_json(msg='instance_description can not start with http:// or https://')
        if len(instance_description) < 2 or len(instance_description) > 256:
            module.fail_json(msg='instance_description is limited to [2-256] characters')

    if db_description:
        if db_description.startswith('http://') or db_description.startswith('https://'):
            module.fail_json(msg='db_description can not start with http:// or https://')
        if len(db_description) < 2 or len(db_description) > 256:
            module.fail_json(msg='db_description is limited to [2-256] characters')

    if instance_network_type:
        if str(instance_network_type) == "VPC":
            if not vpc_id:
                module.fail_json(msg='vpc_id is required to create rds instance when instance_network_type is VPC')
            if not vswitch_id:
                module.fail_json(msg='vswitch_id is required to create rds instance when instance_network_type is VPC')
        if str(instance_network_type) == "Classic":
            if vpc_id:
                module.fail_json(msg='vpc_id is not required to create rds instance when instance_network_type'
                                     ' is Classic')
            if vswitch_id:
                module.fail_json(msg='vswitch_id is not required to create rds instance when instance_network_type '
                                     'is Classic')
    if preferred_backup_time or preferred_backup_period:
        if not (preferred_backup_time and preferred_backup_period):
            module.fail_json(msg='preferred_backup_time and  preferred_backup_period are required to create rds'
                                 ' instance backup policy')

    try:
        changed, result = \
            rds.create_rds_instance(db_engine, engine_version, db_instance_class, db_instance_storage,
                                    instance_net_type, security_ip_list, pay_type, period,zone, instance_description,
                                    used_time, instance_network_type, connection_mode, vpc_id, vswitch_id,
                                    private_ip_address, allocate_public_ip, connection_string_prefix, public_port,
                                    db_name, db_description, character_set_name, maint_window, preferred_backup_time,
                                    preferred_backup_period, backup_retention_period, db_tags, wait, wait_timeout)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to create rds instance, error: {0}'.format(e))

    return changed, result


def change_rds_instance_type(module, rds, instance_id, db_instance_class, db_instance_storage, pay_type):

    """
    Change RDS Instance Type

    :param module:  Ansible module object
    :param rds:  Authenticated rds connection object
    :param instance_id: Id of instances to change
    :param db_instance_class: The instance type of the database
    :param db_instance_storage: Size in gigabytes to change of the DB instance.
    :param pay_type: The pay type of the DB instance.
    :return:
        changed: If instance is changed successfully. the changed para will be set to True else False
        result: detailed server response
    """
    changed = False
    result = []
    if db_instance_storage:
        if str(db_instance_storage).isdigit():
            if int(db_instance_storage) < 5 or int(db_instance_storage) > 2000:
                module.fail_json(msg='db_instance_storage is limited to [5-2000]')
            if int(db_instance_storage) % 5 != 0:
                module.fail_json(msg='db_instance_storage must be multiple of 5GB')
        else:
            module.fail_json(msg='The db_instance_storage must be an integer value, entered value is {0}'.format(
                db_instance_storage))

    try:
        changed, result = rds.change_rds_instance_type(instance_id=instance_id, db_instance_class=db_instance_class,
                                                       db_instance_storage=db_instance_storage, pay_type=pay_type)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to change rds instance type, error: {0}'.format(e))

    return changed, result


def modify_rds_instance(module, rds, instance_id, current_connection_string, connection_string_prefix, port,
                        connection_mode, db_instance_class, db_instance_storage, pay_type, instance_description,
                        security_ip_list, instance_network_type, vpc_id, vswitch_id, maint_window,
                        preferred_backup_time, preferred_backup_period, backup_retention_period):
    """
    Modify RDS Instance

    :param module:  Ansible module object
    :param rds:  Authenticated rds connection object
    :param instance_id: Id of the Instance to modify
    :param current_connection_string: Current connection string of an instance.
    :param connection_string_prefix: Target connection string
    :param port: Target port
    :param connection_mode: Connection mode of the RDS Instance
    :param db_instance_class: The instance type of the database
    :param db_instance_storage: Size in gigabytes of the DB instance to change
    :param pay_type: The pay type of the DB instance.
    :param instance_description: Instance description or remarks, no more than 256 bytes
    :param security_ip_list: List of IP addresses allowed to access all databases of an instance
    :param instance_network_type: The network type of the instance.
    :param vpc_id: The ID of the VPC.
    :param vswitch_id: ID of VSwitch
    :param maint_window: Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.
    :param preferred_backup_time: Backup time, in the format ofHH:mmZ- HH:mm Z.
    :param preferred_backup_period: Backup period
    :param backup_retention_period: Retention days of the backup
    :return:
        changed: If instance is modified successfully. the changed para will be set to True else False
        result: detailed server response
    """
    changed = False
    result = []
    if backup_retention_period:
        if str(backup_retention_period).isdigit():
            if int(backup_retention_period) < 7 or int(backup_retention_period) > 730:
                module.fail_json(msg='backup_retention_period is limited to [7-730]')
        else:
            module.fail_json(msg='The backup_retention_period must be an integer value, entered value is {0}'.format(
                backup_retention_period))
    if instance_description:
        if instance_description.startswith('http://') or instance_description.startswith('https://'):
            module.fail_json(msg='instance_description can not start with http:// or https://')
        if len(instance_description) < 2 or len(instance_description) > 256:
            module.fail_json(msg='instance_description is limited to [2-256]')
    if db_instance_storage:
        if str(db_instance_storage).isdigit():
            if int(db_instance_storage) < 5 or int(db_instance_storage) > 2000:
                module.fail_json(msg='db_instance_storage is limited to [5-2000]')
            if int(db_instance_storage) % 5 != 0:
                module.fail_json(msg='db_instance_storage must be multiple of 5GB')
        else:
            module.fail_json(msg='The db_instance_storage must be an integer value, entered value is {0}'.format(
                db_instance_storage))

    if instance_network_type:
        if str(instance_network_type) == "VPC":
            if not vpc_id:
                module.fail_json(msg='vpc_id is required to modify rds instance when instance_network_type '
                                     'is VPC')
            if not vswitch_id:
                module.fail_json(msg='vswitch_id is required to modify rds instance when instance_network_type '
                                     'is VPC')
        if str(instance_network_type) == "Classic":
            if vpc_id:
                module.fail_json(msg='vpc_id is not required to modify rds instance when instance_network_type '
                                     'is Classic')
            if vswitch_id:
                module.fail_json(msg='vswitch_id is not required to modify rds instance when instance_network_type '
                                     'is Classic')
    if current_connection_string or connection_string_prefix or port:
        if not (current_connection_string and connection_string_prefix and port):
            module.fail_json(msg='current_connection_string, connection_string_prefix, port are required to'
                                 ' modify connection string')
    if preferred_backup_time or preferred_backup_period:
        if not (preferred_backup_time and preferred_backup_period):
            module.fail_json(msg='preferred_backup_time and  preferred_backup_period are required to modify rds '
                                 'instance backup policy')

    try:
        changed, result = rds.modify_rds_instance(instance_id, current_connection_string, connection_string_prefix,
                                                  port, connection_mode, db_instance_class, db_instance_storage,
                                                  pay_type, instance_description, security_ip_list,
                                                  instance_network_type, vpc_id, vswitch_id, maint_window,
                                                  preferred_backup_time, preferred_backup_period,
                                                  backup_retention_period)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)
    except RDSResponseError as e:
        module.fail_json(msg='Unable to modify rds instance , error: {0}'.format(e))
    return changed, result


def create_rds_read_only_instance(module, rds, source_instance, zone, engine_version, db_instance_class,
                                  db_instance_storage, instance_description, pay_type, instance_network_type, vpc_id,
                                  vswitch_id, private_ip_address):
    """
    Create RDS Read-Only Instance

    :param module:  Ansible module object
    :param rds:  Authenticated rds connection object
    :param source_instance: ID of the database to replicate.
    :param zone:  ID of a zone to which an instance belongs
    :param engine_version: Version number of the database engine to use
    :param db_instance_class: The instance type of the database.
    :param db_instance_storage: Size in gigabytes of the initial storage for the DB instance.
    :param instance_description: Instance description or remarks, no more than 256 bytes.
    :param pay_type: The pay type of the DB instance.
    :param instance_network_type: The network type of the instance.
    :param vpc_id: The ID of the VPC
    :param vswitch_id: ID of VSwitch
    :param private_ip_address: IP address of an VPC under VSwitchId.
    :return:
        changed: If ready-only instance is created successfully the changed will be set to True else False
        result: detailed server response
    """

    changed = False
    if not zone:
        module.fail_json(msg='zone is required to create rds read-only instance')
    if not source_instance:
        module.fail_json(msg='source_instance is required to create rds read-only instance')
    if not engine_version:
        module.fail_json(msg='engine_version is required to create rds read-only instance')
    if not db_instance_storage:
        module.fail_json(msg='db_instance_storage is required to create rds read-only instance')
    if not db_instance_class:
        module.fail_json(msg='db_instance_class is required to create rds read-only instance')
    if not pay_type:
        module.fail_json(msg='pay_type is required to create rds read-only instance')
    if db_instance_storage:
        if str(db_instance_storage).isdigit():
            if int(db_instance_storage) < 5 or int(db_instance_storage) > 2000:
                module.fail_json(msg='db_instance_storage is limited to [5-2000]')
            if int(db_instance_storage) % 5 != 0:
                module.fail_json(msg='db_instance_storage must be multiple of 5GB')
        else:
            module.fail_json(msg='The db_instance_storage must be an integer value, entered value is {0}'.format(
                db_instance_storage))

   
    try:
        changed, result = rds.create_rds_read_only_instance(source_instance, zone, engine_version,
                                                            db_instance_class, db_instance_storage,
                                                            instance_description, pay_type, instance_network_type,
                                                            vpc_id, vswitch_id, private_ip_address)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to create rds read-only instance , error: {0}'.format(e))
    return changed, result


def create_database(module, rds, instance_id, db_name, db_description, character_set_name):
    """
    Creates a new database in an instance
    :param module: Ansible module object
    :param rds: Authenticated rds connection object
    :param instance_id: Id of instances
    :param db_name: Name of a database to create within the instance.  If not specified, then no database is created
    :param db_description: Description of a database to create within the instance.  If not specified,
    then no database is created.
    :param character_set_name: Associate the DB instance with a specified character set.
    :return: Result dict of operation
    """
    changed = False
    if not instance_id:
        module.fail_json(msg='instance_id is required for create database')
    if not db_name:
        module.fail_json(msg='db_name is required for create database')
    if not character_set_name:
        module.fail_json(msg='character_set_name is required for create database')
    try:
        changed, result = rds.create_database(instance_id=instance_id, db_name=db_name, db_description=db_description,
                                              character_set_name=character_set_name)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to create database, error: {0}'.format(e))

    return changed, result


def delete_database(module, rds, instance_id, db_name):
    """
    Delete database
    :param module: Ansible module object
    :param rds: Authenticated rds connection object
    :param instance_id: Id of instances
    :param db_name: Name of a database to delete within the instance. If not specified, then no database is deleted
    :return: Result dict of operation
    """
    changed = False
    try:
        if not instance_id:
            module.fail_json(msg='instance_id is required for delete database')
        if not db_name:
            module.fail_json(msg='db_name is required for delete database')
        changed, result = rds.delete_database(instance_id=instance_id, db_name=db_name)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to delete database, error: {0}'.format(e))

    return changed, result


def restart_rds_instance(module, rds, instance_id):
    """
    Restart rds instance
    :param module: Ansible module object
    :param rds: Authenticated rds connection object
    :param instance_id: Id of instances to reboot
    :return: Result dict of operation
    """
    if not instance_id:
        module.fail_json(msg='instance_id is required to restart rds instance')

    changed = False
    try:
        changed, result = rds.restart_rds_instance(instance_id=instance_id)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to restart rds instance, error: {0}'.format(e))

    return changed, result


def release_rds_instance(module, rds, instance_id):
    """
    Release rds instance
    :param module: Ansible module object
    :param rds: Authenticated rds connection object
    :param instance_id: Id of instances to remove
    :return: Result dict of operation
    """
    if not instance_id:
        module.fail_json(msg='instance_id is required to release rds instance')

    changed = False
    try:
        changed, result = rds.release_rds_instance(instance_id=instance_id)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to release rds instance, error: {0}'.format(e))

    return changed, result


def switch_between_primary_standby_database(module, rds, instance_id, node_id, force):
    """
    Switch between primary and standby databases in rds instance
    :param module: Ansible module object
    :param rds: Authenticated rds connection object
    :param instance_id: Id of instances to modify
    :param node_id: Unique ID of a node
    :param force: Yes: forced; No: unforced; default value: unforced
    :return: Result dict of operation
    """
    if not instance_id:
        module.fail_json(msg='instance_id is required to switch between primary '
                             'and standby database for rds instance')
    if not node_id:
        module.fail_json(msg='node_id is required to switch between primary and standby database for rds instance')
        
    changed = False
    result = []
    try:
        changed, result = rds.switch_between_primary_standby_database(instance_id=instance_id, node_id=node_id,
                                                                      force=force)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except RDSResponseError as e:
        module.fail_json(msg='Unable to switch between rds instance, error: {0}'.format(e))

    return changed, result


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        command=dict(default='create', choices=['create', 'delete', 'replicate', 'grant', 'revoke', 'modify',
                                                'reboot', 'switch']),
        alicloud_zone=dict(aliases=['acs_zone', 'ecs_zone', 'zone']),
        instance_id=dict(aliases=['source_instance']),
        db_name=dict(),
        db_description=dict(),
        character_set_name=dict(),
        db_engine=dict(choices=['MySQL', 'SQLServer', 'PostgreSQL', 'PPAS']),
        engine_version=dict(),
        db_instance_class=dict(aliases=['instance_type']),
        db_instance_storage=dict(aliases=['size'], type='int'),
        instance_net_type=dict(choices=['Internet', 'Intranet']),
        instance_description=dict(),
        security_ip_list=dict(),
        pay_type=dict(choices=['Postpaid', 'Prepaid']),
        period=dict(choices=['Year', 'Month']),
        used_time=dict(),
        instance_network_type=dict(aliases=['network_type'], choices=['VPC', 'Classic']),
        connection_mode=dict(),
        vpc_id=dict(),
        vswitch_id=dict(),
        private_ip_address=dict(),
        allocate_public_ip=dict(type='bool'),        
        connection_string_prefix=dict(),
        public_port=dict(type='int'),
        port=dict(type='int'),
        preferred_backup_time=dict(),
        preferred_backup_period=dict(),
        backup_retention_period=dict(type='int'),
        db_tags=dict(type='dict'),
        current_connection_string=dict(),
        maint_window=dict(),
        wait=dict(default='no', choices=['yes', 'Yes', 'no', 'No', "True", "False", "true", "false"]),
        wait_timeout=dict(type='int', default='300'),
        node_id=dict(type='str'),
        force=dict(default='No', type='str', choices=['Yes', 'No'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    rds = rds_connect(module)
    region, acs_connect_kwargs = get_acs_connection_info(module)

    # Get values of variable
    command = module.params['command']
    instance_id = module.params['instance_id']
    db_name = module.params['db_name']
    db_description = module.params['db_description']
    character_set_name = module.params['character_set_name']
    zone = module.params['alicloud_zone']
    db_engine = module.params['db_engine']
    engine_version = module.params['engine_version']
    db_instance_class = module.params['db_instance_class']
    db_instance_storage = module.params['db_instance_storage']
    instance_net_type = module.params['instance_net_type']
    instance_description = module.params['instance_description']
    security_ip_list = module.params['security_ip_list']
    pay_type = module.params['pay_type']
    period = module.params['period']
    used_time = module.params['used_time']
    instance_network_type = module.params['instance_network_type']
    connection_mode = module.params['connection_mode']
    vpc_id = module.params['vpc_id']
    vswitch_id = module.params['vswitch_id']
    private_ip_address = module.params['private_ip_address']
    allocate_public_ip = module.params['allocate_public_ip']    
    connection_string_prefix = module.params['connection_string_prefix']
    public_port = module.params['public_port']
    port = module.params['port']
    maint_window = module.params['maint_window']
    preferred_backup_time = module.params['preferred_backup_time']
    preferred_backup_period = module.params['preferred_backup_period']
    backup_retention_period = module.params['backup_retention_period']
    current_connection_string = module.params['current_connection_string']
    db_tags = module.params['db_tags']
    wait = module.params['wait']
    wait_timeout = module.params['wait_timeout']
    node_id = module.params['node_id']
    force = module.params['force']

    if command == 'create':
        if (instance_id is None) and (db_engine and db_instance_storage and instance_net_type and security_ip_list
                                      and pay_type) is not None:
            (changed, result) = create_rds_instance(module, rds, zone, db_engine, engine_version, db_instance_class,
                                                    db_instance_storage, instance_net_type, instance_description,
                                                    security_ip_list, pay_type, period, used_time,
                                                    instance_network_type, connection_mode, vpc_id, vswitch_id,
                                                    private_ip_address, allocate_public_ip,
                                                    connection_string_prefix, public_port,
                                                    db_name, db_description, character_set_name,
                                                    maint_window, preferred_backup_time,
                                                    preferred_backup_period, backup_retention_period,
                                                    db_tags, wait, wait_timeout)
            module.exit_json(changed=changed, result=result)

        elif instance_id is not None and db_name is not None and character_set_name is not None:

            (changed, result) = create_database(module, rds, instance_id, db_name, db_description, character_set_name)
            module.exit_json(changed=changed, result=result)
        else:
            module.fail_json(msg=[
                {'To create rds instance': 'db_engine, db_instance_storage, instance_net_type, '
                                           'security_ip_list and pay_type parameters are required '
                                           'and instance_id should be None.'},
                {'To create database': 'instance_id, db_name and character_set_name parameters are required.'}               
            ])

    elif command == 'replicate':
        (changed, result) = create_rds_read_only_instance(module, rds, instance_id, zone, engine_version,
                                                          db_instance_class, db_instance_storage,
                                                          instance_description, pay_type, instance_network_type,
                                                          vpc_id, vswitch_id, private_ip_address)
        module.exit_json(changed=changed, result=result)

    elif command == 'modify':
        if instance_id is not None and security_ip_list is not None and db_instance_storage is not None and \
                        pay_type is not None:

            (changed, result) = modify_rds_instance(module, rds, instance_id, current_connection_string,
                                                    connection_string_prefix, port, connection_mode, db_instance_class,
                                                    db_instance_storage, pay_type, instance_description,
                                                    security_ip_list, instance_network_type, vpc_id, vswitch_id,
                                                    maint_window, preferred_backup_time,
                                                    preferred_backup_period, backup_retention_period)
            module.exit_json(changed=changed, result=result)

        elif instance_id is not None and db_instance_storage is not None and pay_type is not None:

            (changed, result) = change_rds_instance_type(module, rds, instance_id, db_instance_class,
                                                         db_instance_storage, pay_type)
            module.exit_json(changed=changed, result=result)

        else:
            module.fail_json(msg=[
                {'To modify rds instance': 'instance_id, security_ip_list, db_instance_storage and '
                                           'pay_type parameters are required.'},
                {' To change rds instance type': 'instance_id, db_instance_storage and'
                                                 ' pay_type parameters are required.'}
            ])

    elif command == 'delete':
        if instance_id is not None and db_name is not None:

            (changed, result) = delete_database(module, rds, instance_id, db_name)
            module.exit_json(changed=changed, result=result)

        elif instance_id is not None:

            (changed, result) = release_rds_instance(module=module, rds=rds, instance_id=instance_id)
            module.exit_json(changed=changed, result=result)

        else:
            module.fail_json(msg=[
                    {'To delete database': 'instance_id and db_name parameters are required.'},
                    {' To release rds instance': 'instance_id parameter is required.'}
                    ])

    elif command == 'reboot':

        (changed, result) = restart_rds_instance(module=module, rds=rds, instance_id=instance_id)
        module.exit_json(changed=changed, result=result)

    elif command == 'switch':

        (changed, result) = switch_between_primary_standby_database(module=module, rds=rds, instance_id=instance_id,
                                                                    node_id=node_id, force=force)
        module.exit_json(changed=changed, result=result)


from ansible.module_utils.basic import *
from ecsutils.ecs import *
main()


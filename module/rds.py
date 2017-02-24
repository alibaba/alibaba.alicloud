#!/usr/bin/python
# This file is part of Ansible
DOCUMENTATION = '''
---
module: rds
short_description: create, delete, or modify an Amazon rds instance
description:
     - Creates, deletes, or modifies rds instances.  When creating an instance it can be either a new instance or a read-only replica of an existing instance.
common options:
  acs_access_key:
    description: The access key.
    required: false
    default: null
    aliases: []
  acs_secret_access_key:
    description: The access secret key.
    required: false
    default: null
    aliases: []
  command:
    description:
      - Specifies the action to take.
    required: true
    choices: [ 'create', 'replicate', 'delete', 'modify' , 'reboot']
    
function: create rds instances
  description: create rds instances.
  command: create
  options:
    region:
      description:
        - The ACS region to use. If not specified then the value of the ECS_REGION environment variable, if any, is used.
      required: true
      aliases: [ 'acs_region', 'ecs_region' ]
    zone:
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
      choices: [ 'MySQL','sqlserver', 'postgres', 'PPAS']
    engine_version:
      description:
        - Version number of the database engine to use. Used only when command=create. If not specified then the current Amazon RDS default engine version is used.
      required: false
      default: null
    instance_type:
      description:
        - The instance type of the database.  Must be specified when command=create. Optional when command=replicate, command=modify. If not specified then the replica inherits the same instance type as the source instance.
      required: false
      default: null
    size:
      description:
        - Size in gigabytes of the initial storage for the DB instance.
      required: true
      default: null
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
    user_time:
      description:
        - The duration of the "Prepaid"
      default: null
      required: (depends on pay_type)
      choices: (depends on period)
    network_type:
      description:
        - The network type of the instance.
      default: Classic
      reqired: false
      choices: ['VPC', 'Classic']
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
    public_connection:
      description:
        - The public connection string.
      default: null
      required: false
    public_port:
      description:
        - The public connection port.
      default: null
      required: false
    private_connection:
      description:
        - The private connection string.
      default: null
      required: false
    private_port:
      description:
        - The private connection port.
      default: null
      required: false
    db_name:
      description:
        - Name of a database to create within the instance.  If not specified then no database is created.
      required: false
      default: null
    db_description:
      description:
        - Description of a database to create within the instance.  If not specified then no database is created.
      required: false
      default: null
    character_set_name:
      description:
        - Associate the DB instance with a specified character set.
      required: false
      default: null
    username:
      description:
        - Master database username. Used only when command=create.
      required: false
      default: null
    password:
      description:
        - Password for the master database username. Used only when command=create or command=modify.
      required: false
      default: null
    maint_window:
      description:
        - "Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.  (Example: Mon:22:00-Mon:23:15) If not specified then a random maintenance window is assigned."
      required: false
      default: null
    backup_window:
      description:
        - Backup window in format of hh24:mi-hh24:mi.  If not specified then a random backup window is assigned.
      required: false
      default: null
    backup_retention:
      description:
        - "Number of days backups are retained.  Set to 0 to disable backups.  Default is 1 day.  Valid range: 0-35.
      required: false
      default: null


function: replicate db instance
  description: create a read-only replica of an existing instance.
  command: replicate
  options:
    source_instance:
      description:
        - ID of the database to replicate.
      required: false
      default: null
    region:
      like command=create
    zone:
      like command=create
    instance_type:
      like command=create
    size:
      like command=create
    instance_description:
      like command=create
    network_type:
      like command=create
    vpc_id:
      like command=create
    vswitch_id:
      like command=create

function: delete rds instances
  description: delete rds instances.
  options:
    instance_name:
    description:
      - Database instance identifier.
    required: false
    default: null

function: modify rds instances
  description: mofify rds instances.
  command: modify
  options:
    instance_name:
      like command=delete
    connection:
      description:
        - The connection string of DB.
      required: false
      default: null
    connection:
      description:
        - The connection port of DB.
      required: false
      default: null
    instance_type:
      like command=create
    size:
      like command=create
    instance_description:
      like command=create
    security_ip_list:
      like command=create
    network_type:
      like command=create
    vpc_id:
      like command=create
    vswitch_id:
      like command=create
    maint_window:
      like command=create
    backup_window:
      like command=create
    backup_retention:
      like command=create

function: reboot rds instances
  description: reboot rds instances.
  command: modify
  options:
    instance_name:
      like command=delete
    force_failover:
      description:
        - If enabled, the reboot is done using a MultiAZ failover.
      required: false
      default: "no"
      choices: [ "yes", "no" ]

  requirements:
      - "python >= 2.6"
      - "footmark"
  author:
      - "xiaozhu"
'''

# FIXME: the command stuff needs a 'state' like alias to make things consistent -- MPD

EXAMPLES = '''
# Basic mysql provisioning example
- rds:
    command: create
    instance_name: new-database
    db_engine: MySQL
    size: 10
    instance_type: db.m1.small
    username: mysql_admin
    password: 1nsecure
    tags:
      Environment: testing
      Application: cms
# Create a read-only replica and wait for it to become available
- rds:
    command: replicate
    instance_name: new-database-replica
    source_instance: new_database
# Delete an instance
- rds:
    command: delete
    instance_name: new-database
# Reboot an instance
- rds
    command: reboot
    instance_name: database
# Modify an instance,
- local_action:
     module: rds
     command: modify
     instance_name: MyNewInstanceName
     region: us-west-2
'''
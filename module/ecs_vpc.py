#!/usr/bin/python
# This file is part of Ansible
DOCUMENTATION = '''
---
module: ecs_vpc
short_description: configure Alicloud virtual private clouds
description:
    - Create or terminates Alicloud virtual private clouds.  This module has a dependency on footmark.
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
  state:
    description: Create or terminate the VPC
    required: true
    choices: [ "present", "absent" ]

function: create vpc
  description: create a vpc.
  options:
    cidr_block:
      description:
        - "The cidr block representing the VPC, e.g. 10.0.0.0/8."
      required: true
      default: "172.16.0.0/12"
      choices: [ "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16" ]
    user_cidr:
      description:
        - "User custom cidr in the VPC."
      required: false
      default: null
    vpc_name:
      description:
        - A VPC name.
      required: false
      default: null
    description:
      description:
        - The VPC description.
      required: false
      default: nll
    subnets:
      description:
        - 'A dictionary array of subnets to add of the form: { cidr: ..., az: ...}. Where az is the desired availability zone of the subnet.'
        - '{"key":"value"}'; keys allowed: 
          - cidr (required:true; default:null)
          - az (required:true, default:null)
          - name (required:false, default:null)
          - description (required:false, default:null).
      required: false
      default: null
    route_tables:
      description:
        - 'A dictionary array of route tables to add of the form: { subnets: [172.22.2.0/24, 172.22.3.0/24,], routes: [{ dest: 0.0.0.0/0, gw: igw, ...},]}. Where the subnets list is those subnets the route table should be associated with, and the routes list is a list of routes to be in the table.  The special keyword for the gw also accepts instance, tunnel, ha_vip and router_interface. '
        - routes key allowed:
          - dest (required:true, default:null)
          - gw (required:false, default:instance_id, if gw is a list, the router is ECMP)
      required: false
      default: null

function: terminate vpc
  description: terminate an vpc.
  options:
    vpc_id:
      description:
        - A VPC id to terminate when state=absent
      required: false
      default: null
'''

EXAMPLES = '''
# Note: None of these examples set acs_access_key, acs_secret_key, or region.
# It is assumed that their matching environment variables are set.
# Basic creation example:
      ecs_vpc:
        state: present
        cidr_block: 172.12.0.0/16
        region: cn-shenzhen
# Full creation example with subnets and optional availability zones.
# The absence or presence of subnets deletes or creates them respectively.
      ecs_vpc:
        state: present
        cidr_block: 172.22.0.0/16
        vpc_name: "Test development"
        subnets:
          - cidr: 172.22.1.0/24
            az: cn-shenzhen-a
          - cidr: 172.22.2.0/24
            az: cn-shenzhen-b
        route_tables:
          - subnets:
              - 172.22.2.0/24
            routes:
              - dest: 0.0.0.0/0
                gw: i-xxxxxxx
          - subnets:
              - 172.22.1.0/24
            routes:
              - dest: 0.0.0.0/0
                gw: i-xxxxxxx
        region: cn-shenzhen
      register: vpc
# Removal of a VPC by id
      ecs_vpc:
        state: absent
        vpc_id: vpc-aaaaaaa
        region: cn-shenzhen
'''

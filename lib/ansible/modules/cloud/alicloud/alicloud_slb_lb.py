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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = """ 
---
module: alicloud_slb_lb
version_added: "2.4"
short_description: Create, Delete, Enable or Disable Server Load Balancer in ECS
options:
  alicloud_region:
    description:
      - The Aliyun Cloud region to use. If not specified then the value of the `ALICLOUD_REGION`, `ACS_REGION`, 
        `ACS_DEFAULT_REGION` or `ECS_REGION` environment variable, if any, is used.
    required: false
    default: null
    aliases: ['acs_region', 'ecs_region', 'region']
  state:
    description: The state of the instance after operating.
    required: false
    default: 'present'
    aliases: [ 'status' ]
    choices: [ 'present', 'absent']
  load_balancer_name:
    description:
        - The name of the server load balancer
    default: null
    required: false
    aliases: [ 'name' ]
  load_balancer_id:
    description:
        - This parameter is required when user wants to perform edit operation in Load Balancer
    default: null
    required: false
    aliases: [ 'ecs_slb' ]
  load_balancer_status:
    description:
        - The lb instance status.
    default: null
    required: false
    choices: ['inactive', 'active']
  address_type:
    description:
        - The address type of the SLB.
    default: internet
    required: false
    aliases: [ 'scheme' ]
    choices: ['internet', 'intranet']
  vswitch_id:
    description:
        - The vswitch id of the VPC instance.
    default: null
    required: false
    aliases: ['subnet_id', 'subnet']
  internet_charge_type:
    description:
        - The charge type of internet.
    default: 'paybytraffic'
    required: false
    choices: ['paybybandwidth', 'paybytraffic']
  master_zone_id:
    description:
        - The main usable area ID of the created Load Balancer can be found by the DescribeZone interface
    default: null
    required: false
  slave_zone_id:
    description:
        - The ID of the standby zone of the created Load Balancer can be found on the DescribeZone interface
    default: null
    required: false
  bandwidth:
    description:
        - Bandwidth peak of the public network instance charged per fixed bandwidth
    required: false
    default: 1
    choices: [ 1-1000 Mbps ]

"""


EXAMPLES = """
# Basic provisioning example to create Load Balancer
- name: create server load balancer
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    load_balancer_name: demo_slb
    address_type: internet
    internet_charge_type: paybytraffic
    state: present
  tasks:
    - name: create server load balancer
      alicloud_slb_lb:
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_name: '{{ load_balancer_name }}'
        address_type: '{{ address_type }}'
        internet_charge_type: '{{ internet_charge_type }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to Modify  SLB Internet Specification
- name: modify server load balancer internet specification
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    load_balancer_id: xxxxxxxxxx
    internet_charge_type: paybytraffic
    bandwidth: 5
  tasks:
    - name: modify server load balancer internet specification
      alicloud_slb_lb:
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        internet_charge_type: '{{ internet_charge_type }}'
        bandwidth: '{{ bandwidth }}'
      register: result
    - debug: var=result

# Basic provisioning example to Delete Server Load Balancer
- name: delete server load balancer
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    load_balancer_id: xxxxxxxxxx
    status : absent
  tasks:
    - name: delete server load balancer
      alicloud_slb_lb:
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        status: '{{ status }}'
      register: result
    - debug: var=result

# Basic provisioning example to set  SLB Status
- name: set server load balancer status
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    load_balancer_id: xxxxxxxxxx
    status: present
    load_balancer_status: active
  tasks:
    - name: set server load balancer
      alicloud_slb_lb:
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        status: '{{ status }}'
        load_balancer_status: '{{ 'load_balancer_status' }}'
      register: result
    - debug: var=result

# Basic provisioning example to set Server Load Balancer Name
- name: set server load balancer name
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    load_balancer_id: xxxxxxxxxx
    load_balancer_name: slb_new_name
    status : present
  tasks:
    - name: set server load balancer name
      alicloud_slb_lb:
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        load_balancer_name: '{{ load_balancer_name }}'
        status: '{{ status }}'
      register: result
    - debug: var=result
"""
RETURN = '''
LoadBalancer:
    description: The slb obj
    return: when create success
    type:dict
    sample:{
        "changed": true, 
        "result": {
            "address": "101.201.178.24", 
            "load_balancer_id": "lb-2ze55q82qclajj6pc2kpt",  
            "network_type": "classic"
        }
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


def create_load_balancer(module, slb, load_balancer_name=None, address_type=None, vswitch_id=None,
                         internet_charge_type=None, master_zone_id=None, slave_zone_id=None, bandwidth=None):
    """
    Create LoadBalancer; generate Server Load Balancer instances, and allocate service addresses and LoadBalancerIds
     according to parameters
    :param module: Ansible module object
    :param slb: Authenticated slb connection object
    :param load_balancer_name: The name of the LoadBalancer
    :param address_type: The AddressType of the LoadBalancer, It allows 'internet' or 'intranet'
        Default: internet
    :param vswitch_id: The vswitch id of VPC instance
    :param internet_charge_type: Charging mode for the public network instance, It allows 'paybybandwidth'
        or 'paybytraffic'. Default: paybytraffic
    :param master_zone_id: Name of master availability zones to enable on this LoadBalancer
    :param  slave_zone_id: Name of slave availability zones to enable on this load balancer
    :param bandwidth: Bandwidth peak of the public network instance charged per fixed bandwidth
        value ranges from 1 to 1000 and default is 1
    :return: Retrun created LoadBalancer details
    """
    changed = False

    if (master_zone_id is None) and (slave_zone_id is not None):
        module.fail_json(msg="provide master_zone_id first")

    result = slb.create_load_balancer(load_balancer_name=load_balancer_name, address_type=address_type,
                                                   vswitch_id=vswitch_id, internet_charge_type=internet_charge_type,
                                                   master_zone_id=master_zone_id, slave_zone_id=slave_zone_id,
                                                   bandwidth=bandwidth)
   
    return  result

def get_load_balancer_objs(slb, load_balancer_id = None, load_balancer_name = None):
    """
    Add Listeners and Backend Servers to Load Balancer
    :param module: Ansible module object
    :param slb: Authenticated slb connection object
    :param load_balancer_id: Id of LoadBalancer    
    :param load_balancer_name: name of LoadBalancer 
    :return: load balancer obj: Ids of LoadBalancers 
    """
    return slb.describe_load_balancers(load_balancer_id = load_balancer_id, load_balancer_name = load_balancer_name)

def main():
    if HAS_FOOTMARK is False:
        print("Footmark required for this module")
        sys.exit(1)
    else:
        argument_spec = ecs_argument_spec()
        argument_spec.update(dict(
            internet_charge_type=dict(choices=['paybybandwidth', 'paybytraffic'], default='paybytraffic'),
            zone_id=dict(aliases=['acs_zone', 'ecs_zone']),
            status=dict(default='present', aliases=['state'], choices=['present', 'absent']),
            load_balancer_name=dict(aliases=['name']),
            load_balancer_id=dict(aliases=['ecs_slb']),
            address_type=dict(default='internet', aliases=['scheme']),
            bandwidth=dict(default=1, type='int'),
            vswitch_id=dict(aliases=['subnet_id', 'subnet']),
            load_balancer_status=dict(default=""),
            master_zone_id=dict(),
            slave_zone_id=dict()
        ))

        module = AnsibleModule(argument_spec=argument_spec)
        slb = slb_connect(module)
        status = module.params['status']
        load_balancer_id = module.params['load_balancer_id']
        load_balancer_name = module.params['load_balancer_name']
        address_type = module.params['address_type']
        vswitch_id = module.params['vswitch_id']
        master_zone_id = module.params['master_zone_id']
        slave_zone_id = module.params['slave_zone_id']
        internet_charge_type = module.params['internet_charge_type']
        load_balancer_status = module.params['load_balancer_status']
        bandwidth = module.params['bandwidth']
        res_objs = []
        changed = False
        result = ["operation failed!"]
        
        if load_balancer_id and load_balancer_name:
            name_test = ""
        else:
            name_test = load_balancer_name
        res_objs = get_load_balancer_objs(slb, load_balancer_id = load_balancer_id, load_balancer_name = name_test)
            
        cur_slb = None
        
        if len(res_objs)==1:
            cur_slb = res_objs[0]            

        if status == "absent" and cur_slb:
            result = cur_slb.delete()
            changed = True    
        elif status == "present" :
            if load_balancer_status and cur_slb:
                #set status
                result = cur_slb.set_status(load_balancer_status)
            elif  load_balancer_name and cur_slb:
                #set name  
                result = cur_slb.modify_name(load_balancer_name)
            elif (internet_charge_type or bandwidth) and cur_slb:
                #set spec
                result = cur_slb.modify_spec(internet_charge_type=internet_charge_type, bandwidth=bandwidth)
            elif len(res_objs) != 1:
                result = create_load_balancer(module=module, slb=slb, load_balancer_name=load_balancer_name,
                                                 address_type=address_type, vswitch_id=vswitch_id,
                                                 internet_charge_type=internet_charge_type,
                                                 master_zone_id=master_zone_id, slave_zone_id=slave_zone_id,
                                                 bandwidth=bandwidth)
            changed = True
            
        else:
            result[0] = ("opration not support")         
        module.exit_json(changed=changed, result=result)   


if __name__ == "__main__":
    main()
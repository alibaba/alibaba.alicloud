#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: alicloud_slb_lb
version_added: "1.0.9"
short_description: Create, Delete, Enable or Disable Server Load Balancer in ECS.
description:
  - Create, Delete, Enable or Disable Server Load Balancer in ECS.
deprecated:
  removed_in: "1.5.0"
  why: Alibaba Cloud module name prefix "ali" will be more concise.
  alternative: Use M(ali_slb_lb) instead.
options:
  state:
    description:
      - The state of the instance after operating.
    default: 'present'
    choices: [ 'present', 'absent', 'running', 'stopped']
  load_balancer_name:
    description:
      - The name of the server load balancer, which is a string of 1 to 80 characters.
        It can contain numerals, "_", "/", "." or "-".
    aliases: [ 'name' ]
  load_balancer_id:
    description:
        - This parameter is required when user wants to perform edit operation in Load Balancer
    aliases: ['id']
  load_balancer_status:
    description:
        - (deprecated) The field has been deprecated from ansible-alicloud v1.1.3.
  address_type:
    description:
        - (deprecated) The field has been deprecated from ansible-alicloud v1.1.3 and 'is_internet' will replace.
  is_internet:
    description:
      - Load balancer network type whether is internet.
    type: bool
    default: Ture
  vswitch_id:
    description:
      - The vswitch id of the VPC instance.
    aliases: ['subnet_id']
  internet_charge_type:
    description:
      - The charge type of internet. It will be ignored when C(is_internet=False)
    default: 'paybytraffic'
    choices: ['paybybandwidth', 'paybytraffic']
  master_zone_id:
    description:
      - The main usable area ID of the created Load Balancer can be found by the DescribeZone interface
  slave_zone_id:
    description:
        - The ID of the standby zone of the created Load Balancer can be found on the DescribeZone interface
  bandwidth:
    description:
      - Bandwidth peak of the public network instance charged per fixed bandwidth. It will be ignored when C(internet_charge_type=paybytraffic)
    default: 1
    choices: [ 1-1000 Mbps ]
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.18"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
  - "Liu Qiang"
"""

EXAMPLES = '''
# Basic provisioning example to create Load Balancer
- name: create server load balancer
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_name: demo_slb
    internet_charge_type: paybytraffic
    state: present
  tasks:
    - name: create server load balancer
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
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
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    internet_charge_type: paybytraffic
    bandwidth: 5
  tasks:
    - name: modify server load balancer internet specification
      alicloud_slb_lb:
        alicloud_region: '{{ alicloud_region }}'
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
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
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    state : absent
  tasks:
    - name: delete server load balancer
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to set Server Load Balancer Name
- name: set server load balancer name
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    load_balancer_name: slb_new_name
    state : present
  tasks:
    - name: set server load balancer name
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        load_balancer_name: '{{ load_balancer_name }}'
        state: '{{ state }}'
      register: result
    - debug: var=result
'''
RETURN = '''
load_balancer:
    description:
      - Describe the current info of  load_balancer after user operate a load_balancer
    returned: on present
    type: string
    sample: {
        "address": "101.201.177.136",
        "bandwidth": null,
        "internet_charge_type": "4",
        "id": "lb-2zekcf2uvij5yw3a7t1c3",
        "name": "test_change_name",
        "status": "active",
        "network_type": "classic"
    }
load_balancer_id:
    description:
      - Unique identification of load balancing instance
    returned: on present or absent
    type: string
    sample: "lb-2zekcf2uvij5yw3a7t1c3"
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


def get_info(lb_obj):
    """
    get info from lb object
    :param lb_obj: lb obj
    :return: info of lb
    """
    return dict(id=lb_obj.load_balancer_id,
                name=lb_obj.load_balancer_name,
                address=lb_obj.address,
                internet_charge_type=lb_obj.internet_charge_type,
                bandwidth=lb_obj.bandwidth,
                load_balancer_status=lb_obj.load_balancer_status,
                network_type=lb_obj.network_type)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        internet_charge_type=dict(type='str', required=False, choices=['paybybandwidth', 'paybytraffic'], default='paybytraffic'),
        state=dict(type='str', required=True, choices=['present', 'absent', 'running', 'stopped']),
        load_balancer_name=dict(type='str', required=False, aliases=['name']),
        load_balancer_id=dict(type='str', required=False, aliases=['id']),
        is_internet=dict(type='bool', required=False, default=True),
        bandwidth=dict(type='int', required=False, default=1),
        vswitch_id=dict(type='str', required=False, aliases=['subnet_id']),
        master_zone_id=dict(type='str', required=False),
        slave_zone_id=dict(type='str', required=False)
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_slb_lb.')

    slb = slb_connect(module)
    state = module.params['state']
    load_balancer_id = module.params['load_balancer_id']
    load_balancer_name = module.params['load_balancer_name']
    is_internet = module.params['is_internet']
    vswitch_id = module.params['vswitch_id']
    master_zone_id = module.params['master_zone_id']
    slave_zone_id = module.params['slave_zone_id']
    internet_charge_type = module.params['internet_charge_type']
    bandwidth = module.params['bandwidth']

    changed = False
    cur_slb = None

    if load_balancer_id and load_balancer_name:
        name_test = ""
    else:
        name_test = load_balancer_name
    res_objs = slb.describe_load_balancers(load_balancer_id=load_balancer_id, load_balancer_name=name_test)
    if len(res_objs) == 1:
        cur_slb = slb.describe_load_balancer_attribute(res_objs[0].id)

    if state == "present":
        if cur_slb:
            if load_balancer_name != cur_slb.name:
                changed = cur_slb.modify_name(load_balancer_name)
                if changed:
                    cur_slb.load_balancer_name = load_balancer_name

            if internet_charge_type != cur_slb.internet_charge_type or \
                    (cur_slb.internet_charge_type == "paybybandwidth" and bandwidth != cur_slb.bandwidth):
                print (cur_slb.__dict__)
                print (cur_slb.internet_charge_type, cur_slb.bandwidth)
                changed = cur_slb.modify_spec(internet_charge_type=internet_charge_type, bandwidth=bandwidth)
                if changed:
                    cur_slb.internet_charge_type = internet_charge_type
                    cur_slb.bandwidth = bandwidth
        else:
            client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
            address_type = "internet"
            if not is_internet:
                address_type = "intranet"
            cur_slb = slb.create_load_balancer(load_balancer_name=load_balancer_name,
                                               address_type=address_type, vswitch_id=vswitch_id,
                                               internet_charge_type=internet_charge_type,
                                               master_zone_id=master_zone_id, slave_zone_id=slave_zone_id,
                                               bandwidth=bandwidth, client_token=client_token)
            changed = True
        module.exit_json(changed=changed, load_balancer=get_info(cur_slb), load_balancer_id=cur_slb.id)

    if not cur_slb:
        module.fail_json(msg="The specified load balancer is not exist. Please check your load_balancer_id or load_balancer_name and try again.")

    if state == "absent":
        changed = cur_slb.delete()
        module.exit_json(changed=changed, load_balancer_id=cur_slb.load_balancer_id)
    if state == "running":
        if cur_slb.status != "active":
            changed = cur_slb.set_status("active")
        if changed:
            cur_slb.load_balancer_status = "active"
        module.exit_json(changed=changed, load_balancer=get_info(cur_slb), load_balancer_id=cur_slb.load_balancer_id)

    if state == "stopped":
        if cur_slb.status != "inactive":
            changed = cur_slb.set_status("inactive")
        if changed:
            cur_slb.load_balancer_status = "inactive"
        module.exit_json(changed=changed, load_balancer=get_info(cur_slb), load_balancer_id=cur_slb.load_balancer_id)


if __name__ == "__main__":
    main()

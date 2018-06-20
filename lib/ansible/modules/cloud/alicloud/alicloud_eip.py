#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com>
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
                    'state': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: alicloud_eip
version_added: "2.5"
short_description: Create eip address and bind it to ECS or SLB instance.
description:
    - Create and release an elastic IP address
    - Associate/disassociate an EIP with ECS or SLB instance
options:
  state:
    description:
      -  state for operating elastic IP address
    choices: ['present', 'absent']
    default: present
  bandwidth:
    description:
      - Maximum outgoing bandwidth to the EIP, measured in Mbps (Mega bit per second)
    default: 5
  internet_charge_type:
    description:
      - Internet charge type of ECS instance
    choices: [ 'PayByBandwidth', 'PayByTraffic']
    default: 'PayByBandwidth'
  ip_address:
    description:
      - The IP address of a previously created EIP. A new EIP will be allocated if it is not specified.
      - If present and instance_id is specified, the EIP is associated with the instance.
      - If absent and instance_id is specified, the EIP is disassociated from the instance.
    aliases: ['ip']
  instance_id:
    description:
      - The id of the device for the EIP. Can be an ECS or SLB Instance id
    aliases: ['device_id']
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# provide some examples to manage eip addresses
- name: requesting eip
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-hongkong
    internet_charge_type: PayByTraffic
    bandwidth: 5
    instance_id: i-23dsefwfv332
  tasks:
    - name: allocating an eip
      alicloud_eip:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        internet_charge_type: '{{ internet_charge_type }}'
        bandwidth: '{{ bandwidth }}'
        state: present
      register: new_eip

    - name: associate the created EIP with an ECS instance
      alicloud_eip:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        ip_address: '{{ new_eip.ip_address }}'
        instance_id: '{{ instance_id }}'
        state: present
      
    - name: disassociate the created EIP with an ECS instance
      alicloud_eip:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        ip_address: '{{ new_eip.ip_address }}'
        instance_id: '{{ instance_id }}'
        state: absent

    - name: disassociate the created EIP with an ECS instance
      alicloud_eip:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        ip_address: '{{ new_eip.ip_address }}'
        state: absent

"""
RETURN = '''
ip_address:
    description: IP address of the allocated EIP
    returned: when present
    type: string
    sample: "123.56.0.206"
allocation_id:
    description: ID of the allocated EIP
    returned: when present
    type: string
    sample: "eip-25877c70x"
instance_id:
    description: ID of the associated device
    returned: when present
    type: string
    sample: "i-aex25877c70x"
eip:
    description: Details about the allocated EIP
    returned: when present
    type: dict
    sample: {
        "allocation_time": "2017-11-13T06:32:50Z", 
        "bandwidth": "7",
        "charge_type": "PostPaid", 
        "id": "eip-gw8wkbxtnl3mh2orfpwm6", 
        "instance_id": "",
        "instance_type": "", 
        "internet_charge_type": "PayByTraffic", 
        "ip_address": "47.91.89.172",
        "operation_locks": {
            "lock_reason": []
        },
        "region_id": "eu-central-1", 
        "status": "Available"
    }
'''

import time
from footmark.exception import VPCResponseError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect, vpc_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_eip(eip_obj):

    if eip_obj:
        return {
            "id": eip_obj.id,
            "allocation_time": eip_obj.allocation_time,
            "bandwidth": eip_obj.bandwidth,
            "instance_id": eip_obj.instance_id,
            "instance_type": eip_obj.instance_type,
            "internet_charge_type": eip_obj.internet_charge_type,
            "ip_address": eip_obj.ip_address,
            "operation_locks": eip_obj.operation_locks,
            "region_id": eip_obj.region_id,
            "status": eip_obj.status,
            "charge_type": eip_obj.charge_type
        }
    return None


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        ip_address=dict(type='str', aliases=['ip']),
        instance_id=dict(type='str', aliases=['device_id']),
        internet_charge_type=dict(type='str', default='PayByBandwidth', choices=['PayByTraffic', 'PayByBandwidth']),
        bandwidth=dict(type='int', default=5)

    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_eip.")
    module = AnsibleModule(argument_spec=argument_spec)
    
    vpc = vpc_connect(module)

    # set values
    state = module.params['state']
    instance_id = module.params['instance_id']
    internet_charge_type = module.params['internet_charge_type']
    ip_address = module.params['ip_address']
    bandwidth = module.params['bandwidth']

    current = None
    changed = False
    if ip_address:
        eips = vpc.get_all_eip_addresses(ip_address=ip_address)
        if eips and len(eips) > 0:
            current = eips[0]

    if state == 'present':
        if not current:
            try:
                client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
                current = vpc.allocate_eip_address(bandwidth=bandwidth, internet_charge_type=internet_charge_type,
                                                   client_token=client_token)
                changed = True
            except VPCResponseError as e:
                module.fail_json(msg='Unable to allocate an eip address, error: {0}'.format(e))

        if bandwidth > 0 and bandwidth != int(current.bandwidth):
            try:
                changed = current.modify(bandwidth=bandwidth)
            except Exception as e:
                module.fail_json(msg="Modify EIP bandwidth failed. Error: {0}".format(e))

        if instance_id and current.status == 'Available':
            try:
                changed = current.associate(instance_id=instance_id)
            except Exception as e:
                module.fail_json(msg="Associate EIP with instance {0} failed. Error: {1}".format(instance_id, e))
        module.exit_json(changed=changed, ip_address=current.ip_address, allocation_id=current.id,
                         instance_id=current.instance_id, eip=get_eip(current))
    else:
        if instance_id:
            try:
                changed = current.disassociate(instance_id=instance_id)
                module.exit_json(changed=changed, ip_address=current.ip_address, allocation_d=current.id, eip=get_eip(current))
            except Exception as e:
                module.fail_json(msg="Disassociate EIP with instance {0} failed. Error: {1}".format(instance_id, e))

        #release
        try:
            changed = current.release()
        except Exception as e:
            module.fail_json(msg="Disassociate EIP with instance {0} failed. Error: {1}".format(instance_id, e))
        module.exit_json(changed=changed)


if __name__ == "__main__":
    main()

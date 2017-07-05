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
module: alicloud_eip
short_description: Requesting eip address, bind eip, unbind eip, modify eip attributes and release eip
options:
  state:
    description:
      -  status for requesting eip addresses, bind eip, unbind eip, modify eip attributes and release eip
    choices: ['present', 'join', 'absent', 'leave']
    required: false
    default: present
  bandwidth:
    description:
      - The rate limit of the EIP, measured in Mbps (Mega bit per second)
    required: false
    default: 5Mbps
  internet_charge_type:
    description:
      - PayByBandwidth and PayByTraffic.
    choices: [ 'PayByBandwidth', 'PayByTraffic']
    required: false
    default: PayByBandwidth
  allocation_id:
    description:
      - The allocation ID of the EIP to be bound, unbound, modify, release.In this condition, allocation_id is reqired. The allocation ID uniquely identifies the EIP
    required: True
    default: null
  instance_id:
    description:
      - The ID of the ECS instance to be bound or unbound. In this condition , instance_id is required.
    required: True
    default: null
"""

EXAMPLES = """
#
# provisioning to requesting eip addresses in EIP
#

# basic provisioning example to requesting eip addresses in EIP
- name: requesting eip
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    internet_charge_type: PayByTraffic
    bandwidth: 5
    status: present
  tasks:
    - name: requesting eip
      alicloud_eip:
        alicloud_region: '{{ alicloud_region }}'
        internet_charge_type: '{{ internet_charge_type }}'
        bandwidth: '{{ bandwidth }}'
        status: '{{ status }}'
      register: result

    - debug: var=result


# basic provisioning example to bind eip
- name: bind eip
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    allocation_id: xxxxxxxxxx
    instance_id: xxxxxxxxxx
    status: join
  tasks:
    - name: bind eip
      alicloud_eip:
        alicloud_region: '{{ alicloud_region }}'
        allocation_id: '{{ allocation_id }}'
        instance_id: '{{ instance_id }}'
        status: '{{ status }}'
      register: result

    - debug: var=result


# basic provisioning example to unbind eip
- name: unbind eip
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    allocation_id: exxxxxxxxxx
    instance_id: xxxxxxxxxx
    state: leave
  tasks:
    - name: unbind eip
      alicloud_eip:
        alicloud_region: '{{ alicloud_region }}'
        allocation_id: '{{ allocation_id }}'
        instance_id: '{{ instance_id }}'
        state: '{{ state }}'
      register: result

    - debug: var=result


# basic provisioning example to modifying eip
- name: modifying eip
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    allocation_id: xxxxxxxxxx
    bandwidth: 3
    status: present
  tasks:
    - name: Modify eip
      alicloud_eip:
        alicloud_region: '{{ alicloud_region }}'
        allocation_id: '{{ allocation_id }}'
        bandwidth: '{{ bandwidth }}'
        status: '{{ status }}'
      register: result

    - debug: var=result


# basic provisioning example to release eip
- name: release eip
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    allocation_id: xxxxxxxxxx
    status: absent
  tasks:
    - name: release eip
      alicloud_eip:
        alicloud_region: '{{ alicloud_region }}'
        allocation_id: '{{ allocation_id }}'
        status: '{{ status }}'
      register: result

    - debug: var=result

"""
RETURN = '''
eip_address:
    description: Assign the flexible public network IP
    returned: when request eip
    type: string
    sample: "123.56.0.206"
allocation_id:
    description: Example of a flexible public network IP
    returned: when request eip 
    type: list
    sample: "eip-25877c70x"
eip:
    description: Details about the ecs instances that were created.
    returned: Query the flexible public IP list
    type: dict
    sample: {
    "EipAddresses": {
        "EipAddress": [
          {
            "AllocationId": "eip-2578g5v5a",
            "AllocationTime": "2014-05-28T03:03:16Z ",
            "Bandwidth": "1",
            "InstanceId": "",
            "InternetChargeType": " PayByBandwidth ",
            "IpAddress": "123.56.0.36",
            "OperationLocks": {
              "LockReason": []
            },
            "RegionId": "cn-beijing",
            "Status": "Available"
          }
        ]
    },
    "PageNumber": 1,
    "PageSize": 10,
    "RequestId": "51BE7822-4121-428A-88F3-262AE4FD868D",
    "TotalCount": 1
    }
'''


import time
from ast import literal_eval
from footmark.exception import VPCResponseError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect, vpc_connect


def requesting_eip_addresses(module, vpc, bandwidth, internet_charge_type):
    """
    requesting for eip address
    :param module: Ansible module object
    :param vpc: authenticated vpc connection object
    :param bandwidth: The rate limit of the EIP. If not specified, it is 5Mbps by default
    :param internet_charge_type: PayByBandwidth and PayByTraffic. The default value is PayByBandwidth.
    :return: a dictionary contains AllocationId, EipAddress and RequestId
    """
    changed = False
    try:
        changed, result = vpc.requesting_eip_addresses(bandwidth=bandwidth, internet_charge_type=internet_charge_type)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(msg=result)

    except VPCResponseError as e:
        module.fail_json(msg='Unable to request eip address, error: {0}'.format(e))
    return changed, result


def bind_eip(module, vpc, allocation_id, instance_id):
    """
    Bind eip address
    :param module: Ansible module object
    :param vpc: authenticated vpc connection object
    :param allocation_id: The allocation ID of the EIP to be bound. The allocation ID uniquely identifies the EIP.
    :param instance_id: The ID of the ECS instance to be bound
    :return: a dictionary of information
    """
    if not allocation_id:
        module.fail_json(msg="allocation_id parameter is needed to bind eip")
    if not instance_id:
        module.fail_json(msg="instance_id parameter is needed to bind eip")

    changed = False
    result = []

    verify_eip_region(module, vpc, allocation_id)

    try:
        changed = vpc.bind_eip(allocation_id=allocation_id, instance_id=instance_id)
        result.append("bind success")
    except VPCResponseError as e:
        module.fail_json(msg='Unable to bind eip, error: {0}'.format(e))

    return changed, result


def unbind_eip(module, vpc, allocation_id, instance_id):
    """
    Unbind eip address
    :param module: Ansible module object
    :param vpc: authenticated vpc connection object
    :param allocation_id: The allocation ID of the EIP to be unbound. The allocation ID uniquely identifies the EIP.
    :param instance_id: The ID of the ECS instance to be unbound
    :return: a dictionary of information
    """
    if not allocation_id:
        module.fail_json(msg="allocation_id parameter is needed to unbind eip")
    if not instance_id:
        module.fail_json(msg="instance_id parameter is needed to unbind eip")

    changed = False
    result = []

    verify_eip_region(module, vpc, allocation_id)

    try:
        changed = vpc.unbind_eip(allocation_id=allocation_id, instance_id=instance_id)
        result.append("unbind success")
    except VPCResponseError as e:
        module.fail_json(msg='Unable to Unbind eip, error: {0}'.format(e))
    return changed, result


def modifying_eip_attributes(module, vpc, allocation_id, bandwidth):
    """
    Modify eip attributes
    :param module: Ansible module object
    :param vpc: authenticated vpc connection object
    :param allocation_id: The allocation ID of the EIP to be bound. The allocation ID uniquely identifies the EIP.
    :param bandwidth: The rate limit of the EIP
    :return: a dictionary of information
    """
    if not allocation_id:
        module.fail_json(msg="allocation_id parameter is needed to modify eip")
    if not bandwidth:
        module.fail_json(msg="bandwidth parameter is needed to modify eip")

    changed = False

    verify_eip_region(module, vpc, allocation_id)

    try:
        changed, result = vpc.modifying_eip_attributes(allocation_id=allocation_id, bandwidth=bandwidth)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(msg=result)

    except VPCResponseError as e:
        module.fail_json(msg='Unable to modify eip attributes, error: {0}'.format(e))
    return changed, result


def release_eip(module, vpc, allocation_id):
    """
    Release eip addresses
    :param module: Ansible module object
    :param vpc: authenticated vpc connection object
    :param allocation_id: The allocation ID of the EIP to be remove. The allocation ID uniquely identifies the EIP.
    :return: a dictionary of information
    """
    if not allocation_id:
        module.fail_json(msg="allocation_id parameter is needed to release eip")

    changed = False
    result = []

    verify_eip_region(module, vpc, allocation_id)

    try:
        changed = vpc.releasing_eip(allocation_id=allocation_id)
        result.append("release success")

    except VPCResponseError as e:
        module.fail_json(msg='Unable to release eip, error: {0}'.format(e))

    return changed, result


def verify_eip_region(module, vpc, allocation_id):
    """
    Verify if eip belongs to the provided region
    :param module: Ansible module object
    :param vpc: authenticated vpc connection object
    :param allocation_id: The allocation ID of the EIP to be remove. The allocation ID uniquely identifies the EIP.
    :return:
    """
    if allocation_id is None:
        module.fail_json("allocation_id is mandatory to verify eip region")

    try:
        eips = vpc.describe_eip_address(allocation_id=allocation_id)

        if eips is None:
            module.fail_json(msg="opration failed")

        if len(eips) != 1:
            module.fail_json(msg="eip with allocation_id " + allocation_id + " does not exist in the provided region")

    except VPCResponseError as e:
        module.fail_json(msg='Unable to verify eip, error: {0}'.format(e))


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        status=dict(default='present', aliases=['state'], choices=['present', 'join', 'absent', 'leave']),
        allocation_id=dict(type='str'),
        instance_id=dict(type='str'),
        internet_charge_type=dict(default='PayByBandwidth', choices=['PayByTraffic', 'PayByBandwidth']),
        bandwidth=dict(type='str')

    ))

    module = AnsibleModule(argument_spec=argument_spec)
    vpc = vpc_connect(module)
    region, acs_connect_kwargs = get_acs_connection_info(module)

    # set values
    status = module.params['status']
    instance_id = module.params['instance_id']
    internet_charge_type = module.params['internet_charge_type']
    allocation_id = module.params['allocation_id']
    bandwidth = module.params['bandwidth']

    if status == 'present':

        if bandwidth is not None:
            try:
                int(bandwidth)
            except Exception as ex:
                module.fail_json(msg="provide valid bandwidth value")

        if (allocation_id and bandwidth) is not None:

            (changed, result) = modifying_eip_attributes(module=module, vpc=vpc, allocation_id=allocation_id,
                                                         bandwidth=bandwidth)
            module.exit_json(changed=changed, result=result)

        else:
            (changed, result) = requesting_eip_addresses(module=module, vpc=vpc,
                                                         bandwidth=bandwidth, internet_charge_type=internet_charge_type)
            module.exit_json(changed=changed, result=result)

    elif status == 'join':

        (changed, result) = bind_eip(module=module, vpc=vpc, allocation_id=allocation_id, instance_id=instance_id)
        module.exit_json(changed=changed, result=result)

    elif status == 'absent':

        (changed, result) = release_eip(module, vpc, allocation_id=allocation_id)
        module.exit_json(changed=changed, result=result)

    elif status == 'leave':

        (changed, result) = unbind_eip(module=module, vpc=vpc, allocation_id=allocation_id, instance_id=instance_id)
        module.exit_json(changed=changed, result=result)

if __name__ == "__main__":
    main()
    
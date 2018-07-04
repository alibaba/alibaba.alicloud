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

DOCUMENTATION = """
---
module: ali_slb_lb_facts
version_added: "1.5.0"
short_description: Gather facts on server load balancer of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the SLB itself.

options:
    load_balancer_name:
      description:
        - A list of server laod balancer names.
      aliases: [ "name"]
    load_balancer_ids:
      description:
        - A list of server load balancer ids.
      aliases: [ "ids" ]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = '''
# Fetch server load balancers according to setting different filters
- name: Fetch server load balancer example
  hosts: localhost
  connection: local
  vars:   
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    load_balancer_ids:
      - lb-dj1tlosv0oqbkho4bitj4
      - lb-dj1e5kwh41n87vkn1pxn5
    load_balancer_name: 
          - test1
          - test
  tasks:
    - name: Find all server load balancers in specified region.
      ali_slb_lb_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'        
      register: all_slb
    - debug: var=all_slb

    - name: Find all server load balancers by ids
      ali_slb_lb_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_ids: '{{ load_balancer_ids }}'
      register: slb_by_id
    - debug: var=slb_by_id
    
    - name: Find all server load balancers by name
      ali_slb_lb_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        name: '{{ load_balancer_name }}'
      register: slb_by_name
    - debug: var=slb_by_name
'''

RETURN = '''
load_balancer_ids:
    description: List all load balancer's id after operating slb.
    returned: when success
    type: list
    sample: [ "lb-dj1oi1h5l74hg22gsnugf", "lb-dj1t1xwn0y9zcr90e52i2" ]
load_balancers:
    description: Details about the server load balancer's that were created.
    returned: when success
    type: list
    sample: [
        {
            "address": "47.95.95.14",
            "address_type": "internet",
            "bandwidth": null,
            "create_time": "2017-10-31T14:44Z",
            "internet_charge_type": "4",
            "load_balancer_id": "lb-dj1oi1h5l74hg22gsnugf",
            "load_balancer_name": "demo_slb2",
            "load_balancer_status": "active",
            "master_zone_id": "cn-beijing-a",
            "network_type": "classic",
            "pay_type": "PayOnDemand",
            "region_id": "cn-beijing",
            "slave_zone_id": "cn-beijing-b",
            "vpc_id": "",
            "vswitch_id": ""
        },
        {
            "address": "47.95.161.24",
            "address_type": "internet",
            "bandwidth": null,
            "create_time": "2017-10-31T13:54Z",
            "internet_charge_type": "4",
            "load_balancer_id": "lb-dj1t1xwn0y9zcr90e52i2",
            "load_balancer_name": "demo_slb",
            "load_balancer_status": "active",
            "master_zone_id": "cn-beijing-a",
            "network_type": "classic",
            "pay_type": "PayOnDemand",
            "region_id": "cn-beijing",
            "slave_zone_id": "cn-beijing-b",
            "vpc_id": "",
            "vswitch_id": ""
        }
    ]
total:
    description: The number of all load balancer's after operating slb.
    returned: when success
    type: int
    sample: 2
'''

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
    return dict(
        load_balancer_id=lb_obj.load_balancer_id,
        load_balancer_name=lb_obj.load_balancer_name,
        address=lb_obj.address,
        internet_charge_type=lb_obj.internet_charge_type,
        bandwidth=lb_obj.bandwidth,
        load_balancer_status=lb_obj.load_balancer_status,
        network_type=lb_obj.network_type,
        master_zone_id=lb_obj.master_zone_id,
        region_id=lb_obj.region_id,
        create_time=lb_obj.create_time,
        pay_type=lb_obj.pay_type,
        slave_zone_id=lb_obj.slave_zone_id,
        address_type=lb_obj.address_type,
        vpc_id=lb_obj.vpc_id,
        resource_group_id=lb_obj.resource_group_id,
        vswitch_id=lb_obj.vswitch_id
    )


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        load_balancer_name=dict(type='list', aliases=['name']),
        load_balancer_ids=dict(type='list', aliases=['ids'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    load_balancer_ids = module.params['load_balancer_ids']
    load_balancer_names = module.params['load_balancer_name']
    result = []
    ids = []

    try:
        slb = slb_connect(module)

        if load_balancer_ids and (not isinstance(load_balancer_ids, list) or len(load_balancer_ids)) < 1:
            module.fail_json(msg='load_balancer_ids should be a list of load balancer ids, aborting')

        if load_balancer_names and (not isinstance(load_balancer_names, list) or len(load_balancer_names)) < 1:
            module.fail_json(msg='load_balancer_name should be a list of load balancer name, aborting')

        # list load balancers by name
        if load_balancer_names:
            result = []
            ids = []
            for  load_balancer_name in load_balancer_names:
                for slb_res in slb.describe_load_balancers(load_balancer_name=load_balancer_name):
                    result.append(get_info(slb_res))
                    ids.append(slb_res.load_balancer_id)

        # list load balancers by ids
        elif load_balancer_ids:
            slb_lb_ids = ",".join(load_balancer_ids)
            for slb_res in slb.describe_load_balancers(load_balancer_id=slb_lb_ids):
                result.append(get_info(slb_res))
                ids.append(slb_res.load_balancer_id)
        # list all load balancers
        else:
            for slb_res in slb.describe_load_balancers():
                result.append(get_info(slb_res))
                ids.append(slb_res.load_balancer_id)

        module.exit_json(changed=False, load_balancer_ids=ids, load_balancers=result, total=len(result))
    except Exception as e:
        module.fail_json(msg="Unable to describe server load balancers, and got an error: {0}.".format(e))


if __name__ == "__main__":
    main()

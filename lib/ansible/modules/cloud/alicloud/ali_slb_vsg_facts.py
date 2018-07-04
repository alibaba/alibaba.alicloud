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
module: ali_slb_vsg_facts
version_added: "1.5.0"
short_description: Gather facts on vserver group of Alibaba Cloud SLB.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the SLB vserver group itself.

options:
    load_balancer_id:
      description:
        - ID of server load balancer.
      required: true
      aliases: [ "lb_id"] 
    vserver_group_ids:
      description:
        - A list of SLB vserver group ids.
      required: false
      aliases: [ "group_ids" ]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch slb server group according to setting different filters
- name: Fetch slb vserver group example
  hosts: localhost
  vars:    
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    load_balancer_id: lb-dj1hv3n9oemvk34evb466
    vserver_group_ids:
      - rsp-dj1lrpsgr8d5v
      - rsp-dj10xmgq31vl0
  tasks:
    - name: Find all vserver gorup in specified slb
      ali_slb_vsg_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
      register: all_vserver_group
    - debug: var=all_vserver_group

    - name: Find all vserver group by ids 
      ali_slb_vsg_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        vserver_group_ids: '{{ vserver_group_ids }}'
      register: vserver_group_by_ids
    - debug: var=vserver_group_by_ids
'''

RETURN = '''
vserver_group_ids:
    description: List all vserver group's id after operating slb vserver group.
    returned: when success
    type: list
    sample: [ "rsp-dj1lrpsgr8d5v", "rsp-dj10xmgq31vl0" ]
vserver_groups:
    description: Details about the slb vserver group that were created.
    returned: when success
    type: list
    sample: [
      {
        "backend_servers": {
          "backend_server": [
            {
              "port": 8282,
              "server_id": "i-2ze35dldjc05dcvezgwk",
              "weight": 100
            },
            {
              "port": 8283,
              "server_id": "i-2zehjm3jvtbkp175c2bt",
              "weight": 100
            }
          ]
        },
        "vserver_group_id": "rsp-dj1lrpsgr8d5v",
        "vserver_group_name": "group_1"
      },
      {
        "backend_servers": {
          "backend_server": [
            {
              "port": 8085,
              "server_id": "i-2zehjm3jvtbkp175c2bt",
              "weight": 100
            },
            {
              "port": 8086,
              "server_id": "i-2ze35dldjc05dcvezgwk",
              "weight": 100
            }
          ]
        },
        "vserver_group_id": "rsp-dj10xmgq31vl0",
        "vserver_group_name": "group_2"
      }
    ]
total:
    description: The number of all vserver group after operating slb.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, slb_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import SLBResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_info(obj):
    """
    get info from vsg object
    :param obj: vsg obj
    :return: res: info of vsg
    """
    res = {'vserver_group_id': obj.vserver_group_id}

    if hasattr(obj, 'backend_servers'):
        res['backend_servers'] = obj.backend_servers
    if hasattr(obj, 'vserver_group_name'):
        res['vserver_group_name'] = obj.vserver_group_name
    return res


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        load_balancer_id=dict(type='str', aliases=['lb_id'], required=True),
        vserver_group_ids=dict(type='list', aliases=['group_ids'])
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    load_balancer_id = module.params['load_balancer_id']
    vserver_group_ids = module.params['vserver_group_ids']
    ids = []
    result = []
    all_vserver_group_ids = []

    if vserver_group_ids and (not isinstance(vserver_group_ids, list) or len(vserver_group_ids)) < 1:
        module.fail_json(msg='vserver_group_ids should be a list of vserver group ids, aborting')

    try:
        slb = slb_connect(module)
        laod_balancer = slb.describe_load_balancers(load_balancer_id=load_balancer_id)

        if laod_balancer and len(laod_balancer) == 1:

            # list all vserver groups in selected load balancer
            for vserver_group_obj in slb.describe_vserver_groups(load_balancer_id=load_balancer_id):
                all_vserver_group_ids.append(vserver_group_obj.vserver_group_id)

            # if list of vserver group id provided
            if vserver_group_ids:

                for vserver_group_id in vserver_group_ids:

                    # check whether provided vserver grooup id is valid or not
                    if vserver_group_id in all_vserver_group_ids:
                        vserver_group = slb.describe_vserver_group_attribute(vserver_group_id)
                        result.append(get_info(vserver_group))
                        ids.append(vserver_group_id)

            # list all vserver group in specified slb
            else:
                for vserver_group_id in all_vserver_group_ids:
                    vserver_group = slb.describe_vserver_group_attribute(vserver_group_id)
                    result.append(get_info(vserver_group))
                    ids.append(vserver_group.vserver_group_id)

            module.exit_json(changed=False, vserver_group_ids=ids,
                             vserver_groups=result, total=len(result))
        else:
            module.fail_json(msg="Unable to describe slb vserver groups, invalid load balancer id")
    except Exception as e:
        module.fail_json(msg=str("Unable to describe slb vserver group, error:{0}".format(e)))


if __name__ == '__main__':
    main()

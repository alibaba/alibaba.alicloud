#!/usr/bin/python
# Copyright (c) 2017 Ansible Project
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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_slb_listener_facts
version_added: "1.5.0"
short_description: Gather facts on listener of Alibaba Cloud SLB.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the SLB listeners itself.

options:
    load_balancer_id:
      description:
        - ID of server load balancer.
      required: true
      aliases: [ "lb_id" ]      
    listener_type:
      description:
        - User expects the type of operation listener.
      required: true
      choices: [ 'http', 'https', 'tcp', 'udp']
    listener_port:
      description:
        - Port used by the Server Load Balancer instance frontend
      required: true
      choices: [1~65535]
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
"""

EXAMPLES = """
# Fetch SLB listener details according to setting different filters
- name: Fetch SLB listener details example
  hosts: localhost
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    load_balancer_id: lb-dj1jywbux1zslfna6pvnv
    listener_type: http
    listener_port: 8085
  tasks:
    - name: Fetch SLB listener details example
      ali_slb_listener_facts:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        listener_type: '{{ listener_type }}'
        listener_port: '{{ listener_port }}'
      register: result
    - debug: var=result
"""

RETURN = '''
listener:
    description: Details about SLB listener that were created.
    returned: when success
    type: dict
    sample: {
        "backend_server_port": 8085,
        "bandwidth": 1,
        "listener_port": 8085,
        "listener_type": null,
        "persistence_timeout": null,
        "schedule": null,
        "server_certificate_id": null,
        "status": "stopped",
        "sticky_session": "off"
    }
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


def get_info(obj):
    """
    get info from lb object
    :param obj: lb obj
    :return: info of lb
    """
    result = dict(listener_port=obj.listener_port,
                  backend_server_port=obj.backend_server_port,
                  bandwidth=obj.bandwidth,
                  status=obj.status,
                  schedule=obj.schedule,
                  listener_type=obj.listener_type)

    if hasattr(obj, 'server_certificate_id'):
        result['server_certificate_id'] = obj.server_certificate_id
    if hasattr(obj, 'sticky_session'):
        result['sticky_session'] = obj.sticky_session
    if hasattr(obj, 'persistence_timeout'):
        result['persistence_timeout'] = obj.persistence_timeout
    return result


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        listener_port=dict(type='int', required=True, choices=[i for i in range(1, 65536)]),
		load_balancer_id=dict(type='str', aliases=['lb_id']),
        listener_type=dict(type='str', choices=['http', 'https', 'tcp', 'udp'])
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    load_balancer_id = module.params['load_balancer_id']
    listener_port = module.params['listener_port']
    listener_type = module.params['listener_type']

    try:
        slb = slb_connect(module)

        # check whether server load balancer exist or not
        laod_balancer = slb.describe_load_balancers(load_balancer_id=load_balancer_id)
        if laod_balancer and len(laod_balancer) == 1:

            # list load balancers listeners
            listener = slb.describe_load_balancer_listener_attribute(load_balancer_id,
                                                                     listener_port,
                                                                     listener_type)
            if listener is None:
                module.fail_json(msg="Unable to describe slb listeners, no listeners found")
            else:
                module.exit_json(changed=False, listener=get_info(listener))
        else:
            module.fail_json(msg="Unable to describe slb listeners, invalid load balancer id")
    except Exception as e:
        module.fail_json(msg="Unable to describe slb listeners, and got an error: {0}.".format(e))


if __name__ == "__main__":
    main()

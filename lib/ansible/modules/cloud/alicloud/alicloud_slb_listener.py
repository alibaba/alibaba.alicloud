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
module: alicloud_slb_listener
version_added: "2.5"
short_description: Create, Delete, Start or Stop Server Load Balancer Listener in ECS
description:
  - Create, Delete, Start or Stop Server Load Balancer Listener in ECS
options:
  state:
    description:
      - The state of the instance after operating.
    required: true
    choices: [ 'present', 'absent', 'list', 'running', 'stopped']
  listener_type:
    description:
      - User expects the type of operation listener.
    required: true
    choices: [ 'http', 'https', 'tcp', 'udp']
  load_balancer_id:
    description:
      - The unique ID of an Server Load Balancer instance
    required: true
  listener_port:
    description:
      - Port used by the Server Load Balancer instance frontend
    required: true
    choices: [1~65535]
  bandwidth:
    description:
      - Bandwidth peak of Listener
    choices: [1-1000]
  backend_server_port:
    description:
      - Port used by the Server Load Balancer instance backend port
    choices: [1~65535]
  persistence_timeout:
    description:
      - Timeout of connection persistence.
    default: 0
    choices: [0~3600]
  scheduler:
    description:
      - Scheduling algorithm.
    default: 'wrr'
    choices: ['wlc', 'wrr']
  sticky_session:
    description:
      - Whether to enable session persistence.
    choices: ['on', 'off']
  sticky_session_type:
    description:
      - Mode for handling the cookie. Required when C(sticky_session='on').
    choices: ['server', 'insert']
  cookie_timeout:
    description:
      - Cookie timeout, Required when C(sticky_session='on', sticky_session_type='insert')
    choices: [ 1~86400]
  cookie:
    description:
      - The cookie configured on the server. Required when C(sticky_session='on', sticky_session_type='server')
  health_check:
    description:
      - Whether to enable health check.
    choices: ['on', 'off']
  health_check_domain:
    description:
      - Domain name used for health check. Required when C(health_check='on').
    choices: [$ _ip, user-defined string, '']
  health_check_uri:
    description:
      - URI used for health check. Required when C(health_check='on').
  health_check_connect_port:
    description:
      - Port used for health check. Required when C(health_check='on').
        When the parameter is set to -520, it means the backend server port (Backen dServerPort) is used.
    choices: [1~65535]
  healthy_threshold:
    description:
      - Threshold determining the result of the health check is success.
        Namely, after how many successive successful health checks,
        the health check result of the backend server is changed from fail to success. Required when C(health_check='on').
    choices: [1-10]
  unhealthy_threshold:
    description:
      - Threshold determining the result of the health check is fail.
        Namely, after how many successive failed health checks,
        the health check result of the backend server is changed from success to fail. Required when C(health_check='on').
    choices: [1-10]
  health_check_timeout:
    description:
      - TMaximum timeout of each health check response. Required when C(health_check='on').
    choices: [1-50]
  health_check_interval:
    description:
      - Time interval of health checks. Required when C(health_check='on').
    choices: [1-5]
  health_check_http_code:
    description:
      - Regular health check HTTP status code. Multiple codes are segmented by ",". Required when C(health_check='on').
    default: http_2xx
    choices: ['http_2xx','http_3xx', 'http_4xx', 'http_5xx']
  vserver_group_id:
    description:
      - Virtual server group ID, when the VserverGroup is on, the incoming VServerGroupId value takes effect.
  gzip:
    description:
      - Whether to open the Gzip compression. If open, the specific file types will be compressed, If not, any type of file won't be compressed.
    default: on
    choices: ['on','off']
  master_slave_server_group_id:
    description:
      - Master slave server group. Virtual server group ID and master-slave server group ID cannot be both used at the same time.
  source_items:
    description:
      - Access control list. Required when RemoveListenerWhiteListItem or AddListenerWhiteListItem.
  server_certificate_id:
    description:
      - Security certificate ID, required when C(listener_type=https)
  access_control_status:
    description:
      - Whether or not access control is enabled
    choices: ['on', 'off']
  health_check_connect_timeout:
    description:
      - Health check connection timeout
    default: 5
    choices: [1 ~ 50]
  ca_certificate_id:
    description:
      - CA certificate ID
  syn_proxy:
    description:
      - whether open SynProxy
    default: 'disable'
    choices: ['disable', 'enable']
  health_check_type:
    description:
      - Health check type
    default: 'tcp'
    choices: ['tcp', 'http']
  vserver_group:
    description:
      - Whether to use the virtual server group, VserverGroup and MasterSlaveServerGroup only allow one value to be on.
    default: 'off'
    choices: ['on', 'off']
  master_slave_server_group:
    description:
      - Whether the main standby server group is used, VserverGroup and MasterSlaveServerGroup only allow one value to be on
    default: 'off'
    choices: ['on', 'off']
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# Basic provisioning example to create Load Balancer Listener
- name: create server load balancer http listener
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    backend_server_port: 80
    state: present
  tasks:
    - name: create server load balancer listener
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        backend_server_port: '{{ backend_server_port }}'
        bandwidth: 1
        sticky_session: off
        health_check: off
        listener_type: http
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to stop Load Balancer Listener
- name: stop server load balancer listener
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: stopped
  tasks:
    - name: stop server load balancer listener
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        listener_type: http
        listener_port: '{{ listener_port }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to start Load Balancer Listener
- name: start server load balancer listener
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: running
  tasks:
    - name: start server load balancer listener
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        listener_type: http
        listener_port: '{{ listener_port }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to set listener access control status
- name: set listener access control status
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: present
  tasks:
    - name: set listener access control status
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        listener_type: http
        access_control_status: on
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to add white list item
- name: add white list item
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: present
  tasks:
    - name: add white list item
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        listener_type: http
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        source_items: 1.1.1.1
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to remove white list item
- name: remove white list item
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: absent
  tasks:
    - name: remove white list item
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        listener_type: http
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        source_items: 1.1.1.1
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to set listener attribute
- name: set listener attribute
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: present
  tasks:
    - name: set listener attribute
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        listener_type: http
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        bandwidth: 4
        scheduler: wlc
        sticky_session: off
        health_check: off
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to list listener attribute
- name: list listener attribute
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: list
  tasks:
    - name: list listener attribute
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        listener_type: http
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# Basic provisioning example to delete listener
- name: delete listener
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-beijing
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    load_balancer_id: <your-specified-load-balancer>
    listener_port: 80
    state: absent
  tasks:
    - name: delete listener
      alicloud_slb_lb:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        load_balancer_id: '{{ load_balancer_id }}'
        listener_port: '{{ listener_port }}'
        listener_type: http
        state: '{{ state }}'
      register: result
    - debug: var=result
"""
RETURN = '''
listener:
    description:
        - The info of load balancer listener
    returned: when success
    type: dict
    sample: {
        "backend_server_port": 80,
        "bandwidth": 4,
        "listener_port": 80,
        "schedule": null,
        "server_certificate_id": null,
        "status": "running",
        "sticky_session": "off",
        "xforwarded_for": null
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


def get_info(obj):
    """
    get info from lb object
    :param lb_ls_obj: lb obj
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
        state=dict(type='str', required=True, choices=['present', 'absent', 'list', 'stopped', 'running']),
        load_balancer_id=dict(type='str', required=True, aliases=['id']),
        backend_server_port=dict(type='int', choices=[i for i in range(1, 65536)]),
        bandwidth=dict(type='int', choices=([i for i in range(1, 1001)]).append(-1)),
        sticky_session=dict(type='str', choices=['on', 'off']),
        listener_type=dict(type='str', choices=['http', 'https', 'tcp', 'udp']),
        health_check=dict(type='str', choices=['on', 'off']),
        access_control_status=dict(type='str', choices=['on', 'off']),
        scheduler=dict(type='str', default='wrr', choices=['wrr', 'wlc']),
        source_items=dict(type='str'),
        sticky_session_type=dict(type='str', choices=['insert', 'server']),
        cookie_timeout=dict(type='str', choices=[i for i in range(1, 86401)]),
        cookie=dict(type='str'),
        health_check_domain=dict(type='str'),
        health_check_uri=dict(type='str'),
        health_check_connect_port=dict(type='int', choices=([i for i in range(1, 65536)]).append(-520)),
        healthy_threshold=dict(type='int', choices=[i for i in range(1, 11)]),
        unhealthy_threshold=dict(type='int', choices=[i for i in range(1, 11)]),
        health_check_timeout=dict(type='int', choices=[i for i in range(1, 51)]),
        health_check_interval=dict(type='int', choices=[i for i in range(1, 6)]),
        health_check_http_code=dict(type='str'),
        vserver_group_id=dict(type='str'),
        gzip=dict(type='str', default='on', choices=['on', 'off']),
        server_certificate_id=dict(type='str'),
        master_slave_server_group_id=dict(type='str'),
        persistence_timeout=dict(type='int', default=0, choices=[i for i in range(0, 3601)]),
        health_check_connect_timeout=dict(type='int', default=5, choices=[i for i in range(0, 51)]),
        ca_certificate_id=dict(type='str'),
        syn_proxy=dict(type='str', default='disable', choice=['disable', 'enable']),
        health_check_type=dict(type='str', default='tcp', choice=['tcp', 'http']),
        vserver_group=dict(type='str', default='off', choice=['on', 'off']),
        master_slave_server_group=dict(type='str', default='off', choice=['on', 'off'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_slb_listener.')

    slb = slb_connect(module)
    state = module.params['state']
    load_balancer_id = module.params['load_balancer_id']
    listener_port = module.params['listener_port']
    backend_server_port = module.params['backend_server_port']
    bandwidth = module.params['bandwidth']
    sticky_session = module.params['sticky_session']
    listener_type = module.params['listener_type']
    health_check = module.params['health_check']
    access_control_status = module.params['access_control_status']
    scheduler = module.params['scheduler']
    source_items = module.params['source_items']
    sticky_session_type = module.params['sticky_session_type']
    cookie_timeout = module.params['cookie_timeout']
    cookie = module.params['cookie']
    health_check_domain = module.params['health_check_domain']
    health_check_uri = module.params['health_check_uri']
    health_check_connect_port = module.params['health_check_connect_port']
    healthy_threshold = module.params['healthy_threshold']
    unhealthy_threshold = module.params['unhealthy_threshold']
    health_check_timeout = module.params['health_check_timeout']
    health_check_interval = module.params['health_check_interval']
    health_check_http_code = module.params['health_check_http_code']
    vserver_group_id = module.params['vserver_group_id']
    gzip = module.params['gzip']
    server_certificate_id = module.params['server_certificate_id']
    master_slave_server_group_id = module.params['master_slave_server_group_id']
    persistence_timeout = module.params['persistence_timeout']
    health_check_connect_timeout = module.params['health_check_connect_timeout']
    ca_certificate_id = module.params['ca_certificate_id']
    syn_proxy = module.params['syn_proxy']
    health_check_type = module.params['health_check_type']
    vserver_group = module.params['vserver_group']
    master_slave_server_group = module.params['master_slave_server_group']

    changed = False
    current_listener = slb.describe_load_balancer_listener_attribute(load_balancer_id, listener_port, listener_type)

    if state == "present":
        if current_listener:
            if access_control_status:
                # set access_control_status
                if access_control_status == "on":
                    access_control_status = "open_white_list"
                elif access_control_status == "off":
                    access_control_status = "close"
                changed = current_listener.set_access_control_status(load_balancer_id, access_control_status)
            elif source_items:
                # add listener_white_list_item
                changed = current_listener.add_white_list_item(load_balancer_id, source_items)
            else:
                # set attribute
                changed = current_listener.set_attribute(load_balancer_id=load_balancer_id,
                                                         bandwidth=bandwidth,
                                                         sticky_session=sticky_session,
                                                         listener_type=listener_type,
                                                         health_check=health_check,
                                                         scheduler=scheduler,
                                                         sticky_session_type=sticky_session_type,
                                                         cookie_timeout=cookie_timeout,
                                                         cookie=cookie,
                                                         health_check_domain=health_check_domain,
                                                         health_check_uri=health_check_uri,
                                                         health_check_connect_port=health_check_connect_port,
                                                         healthy_threshold=healthy_threshold,
                                                         unhealthy_threshold=unhealthy_threshold,
                                                         health_check_timeout=health_check_timeout,
                                                         health_check_interval=health_check_interval,
                                                         health_check_http_code=health_check_http_code,
                                                         vserver_group_id=vserver_group_id,
                                                         gzip=gzip,
                                                         server_certificate_id=server_certificate_id,
                                                         master_slave_server_group_id=master_slave_server_group_id,
                                                         persistence_timeout=persistence_timeout,
                                                         health_check_connect_timeout=health_check_connect_timeout,
                                                         ca_certificate_id=ca_certificate_id,
                                                         syn_proxy=syn_proxy,
                                                         health_check_type=health_check_type,
                                                         vserver_group=vserver_group,
                                                         master_slave_server_group=master_slave_server_group)
            module.exit_json(changed=changed, listener=get_info(current_listener.describe_attribute(load_balancer_id, listener_type)))
        else:
            changed = slb.create_load_balancer_listener(load_balancer_id=load_balancer_id,
                                                        listener_port=listener_port,
                                                        backend_server_port=backend_server_port,
                                                        bandwidth=bandwidth,
                                                        sticky_session=sticky_session,
                                                        listener_type=listener_type,
                                                        health_check=health_check,
                                                        scheduler=scheduler,
                                                        sticky_session_type=sticky_session_type,
                                                        cookie_timeout=cookie_timeout,
                                                        cookie=cookie,
                                                        health_check_domain=health_check_domain,
                                                        health_check_uri=health_check_uri,
                                                        health_check_connect_port=health_check_connect_port,
                                                        healthy_threshold=healthy_threshold,
                                                        unhealthy_threshold=unhealthy_threshold,
                                                        health_check_timeout=health_check_timeout,
                                                        health_check_interval=health_check_interval,
                                                        health_check_http_code=health_check_http_code,
                                                        vserver_group_id=vserver_group_id,
                                                        gzip=gzip,
                                                        server_certificate_id=server_certificate_id,
                                                        master_slave_server_group_id=master_slave_server_group_id,
                                                        persistence_timeout=persistence_timeout,
                                                        health_check_connect_timeout=health_check_connect_timeout,
                                                        ca_certificate_id=ca_certificate_id)
            new_current_listener = slb.describe_load_balancer_listener_attribute(load_balancer_id, listener_port, listener_type)
            module.exit_json(changed=changed, listener=get_info(new_current_listener))
    if not current_listener:
        module.fail_json(msg="The specified load balancer listener is not exist. Please check your load_balancer_id or listener_port and try again.")
    if state == "absent":
        if source_items:
            # remove listener white list item
            changed = current_listener.remove_white_list_item(load_balancer_id, source_items)
            module.exit_json(changed=changed, listener=get_info(current_listener.describe_attribute(load_balancer_id, listener_type)))
        # delete
        changed = current_listener.delete(load_balancer_id)
        module.exit_json(changed=changed, listener=get_info(current_listener))
    if state == "running":
        # start
        changed = current_listener.start(load_balancer_id)
        module.exit_json(changed=changed, listener=get_info(current_listener.describe_attribute(load_balancer_id, listener_type)))
    if state == "stopped":
        # stop
        changed = current_listener.stop(load_balancer_id)
        module.exit_json(changed=changed, listener=get_info(current_listener.describe_attribute(load_balancer_id, listener_type)))
    if state == 'list':
        # list attribute
        module.exit_json(changed=True, listener=get_info(current_listener))

if __name__ == "__main__":
    main()

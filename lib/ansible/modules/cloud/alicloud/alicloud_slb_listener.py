#!/usr/bin/python
# -*- coding: utf-8 -*-
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
module: alicloud_slb_listener
version_added: "2.4"
short_description: Create, Delete, Start or Stop Server Load Balancer Listener in ECS
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
    required: true
    default: 'present'
    choices: [ 'present', 'absent', 'list', 'running', 'stopped']
  listener_type:
    description: User expects the type of operation listener.
    required: true
    default: null
    type: string
    choices: [ 'http', 'https', 'tcp', 'udp']
  load_balancer_id:
    description:
        - The unique ID of an Server Load Balancer instance
    default: null
    required: true
  listener_port:
    description:
        - Port used by the Server Load Balancer instance frontend
    default: null
    required: true
    choices: [1~65535]
  bandwidth:
    description:
        - Bandwidth peak of Listener
    required: true
    default: null
    choices: [1-1000]
  backend_server_port:
    description:
        - Port used by the Server Load Balancer instance backend port
    default: null
    required: true
    choices: [1~65535]
  persistence_timeout:
    description:
        - Timeout of connection persistence.
    default: 0
    required: false
    choices: [0~3600]
    type: int
  scheduler:
    description:
        - Scheduling algorithm.
    default: wrr
    required: false
    choices: ['wlc', 'wrr']
  sticky_session:
    description:
        - Whether to enable session persistence.
    default: null
    required: true
    choices: ['on', 'off']
  sticky_session_type:
    description:
        - Mode for handling the cookie. Required when C(sticky_session='on').
    default: null
    required: false
    choices: ['server', 'insert']
  cookie_timeout:
    description:
        - Cookie timeout, Required when C(sticky_session='on', sticky_session_type='insert')
    default: null
    required: false
    choices:[ 1~86400]
  cookie:
    description:
        - The cookie configured on the server. Required when C(sticky_session='on', sticky_session_type='server')
    default: null
    required: false
    type: string
  health_check:
    description:
        - Whether to enable health check.
    default: null
    required: true
    choices: ['on', 'off']
  health_check_domain:
    description:
        - Domain name used for health check. Required when C(health_check='on').
    default: null
    required: false
    choices: ['on', 'off']
  health_check_uri:
    description:
        - URI used for health check. Required when C(health_check='on').
    default: null
    required: false
    type: string
  health_check_connect_port:
    description:
        - Port used for health check. Required when C(health_check='on').When the parameter is set to -520, it means the backend server port (Backen dServerPort) is used.
    default: null
    required: false
    type: int
    choices: [1~65535] or [-520]
  healthy_threshold:
    description:
        - Threshold determining the result of the health check is success. Namely, after how many successive successful health checks, the health check result of the backend server is changed from fail to success. Required when C(health_check='on'). 
    default: null
    required: false
    type: int
    choices: [1-10]
  unhealthy_threshold:
    description:
        - Threshold determining the result of the health check is fail. Namely, after how many successive failed health checks, the health check result of the backend server is changed from success to fail. Required when C(health_check='on').
    default: null
    required: false
    type: int
    choices: [1-10]
  health_check_timeout:
    description:
        - TMaximum timeout of each health check response. Required when C(health_check='on').
    default: null
    required: false
    type: int
    choices: [1-50]
  health_check_interval:
    description:
        - Time interval of health checks. Required when C(health_check='on').
    default: null
    required: false
    type: int
    choices: [1-5]
  health_check_http_code:
    description:
        - Regular health check HTTP status code. Multiple codes are segmented by ",". Required when C(health_check='on').
    default: http_2xx
    required: false
    type: string
    choices: ['http_2xx','http_3xx', 'http_4xx', 'http_5xx']
  vserver_group_id:
    description:
        - Virtual server group ID.
    default: null
    required: false
    type: string
  gzip:
    description:
        -Whether to open the Gzip compression. If open, the specific file types will be compressed; If not, any type of file won鈥檛 be compressed.
    default: on
    required: false
    type: string
    choices: ['on','off']
  master_slave_server_group_id:
    description:
        -Master-slave server group. Virtual server group ID and master-slave server group ID cannot be both used at the same time.
    required: false
    type: string
  source_items:
    description:
        -Access control list. Required when RemoveListenerWhiteListItem or AddListenerWhiteListItem .
    required: false
    type: string
  server_certificate_id:
    description:
        -Security certificate ID, required when C(listener_type=https)
    required: false
    type: string
  access_control_status:
    description:
        -Whether or not access control is enabled
    required: false
    type: string
    choices: ['open_white_list', 'close']
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
    listener_port: <your-specified-load-balancer-frontend-port>
    backend_server_port: <your-specified-load-balancer-backend-port>
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
    listener_port: <your-specified-load-balancer-frontend-port>
    backend_server_port: <your-specified-load-balancer-backend-port>
    state: stop
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
    listener_port: <your-specified-load-balancer-frontend-port>
    backend_server_port: <your-specified-load-balancer-backend-port>
    state: start
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
    listener_port: <your-specified-load-balancer-frontend-port>
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
        access_control_status: open_white_list
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
    listener_port: <your-specified-load-balancer-frontend-port>
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
    listener_port: <your-specified-load-balancer-frontend-port>
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
    listener_port: <your-specified-load-balancer-frontend-port>
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
    listener_port: <your-specified-load-balancer-frontend-port>
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
    listener_port: <your-specified-load-balancer-frontend-port>
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
load_balancer_id:
    description:
        - Unique identification of load balancing instance
    returned: on present or absent
    type: string
    sample: "lb-2zekcf2uvij5yw3a7t1c3"
listener:
    description:
        - The info of load balancer listener
    returned: on list
    type: dict
    sample: {
        "backend_server_port": 80,
        "bandwidth": 4,
        "listener_port": 80,
        "schedule": null,
        "server_certificate_id": null,
        "status": "running",
        "sticky_session": "off",
        "x_forwarded_for": null
    },
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
    result = {} 

    result['listener_port'] = obj.listener_port
    result['backend_server_port'] = obj.backend_server_port
    result['bandwidth'] = obj.bandwidth
    result['status'] = obj.status
    result['schedule'] = obj.schedule
    if hasattr(obj, 'server_certificate_id'):
        result['server_certificate_id'] = obj.server_certificate_id
    if hasattr(obj, 'sticky_session'):
        result['sticky_session'] = obj.sticky_session
    if hasattr(obj, 'persistence_timeout'):
        result['persistence_timeout'] = obj.persistence_timeout
    return result

def assemble_request_data(listener, key, value):
    """
    assemble request data
    :param listener: reqest data
    :param var: param
    :return: info of request data
    """
    if value:
        listener[key] = value
    return listener

def main():
    if HAS_FOOTMARK is False:
        module.fail_json("Footmark required for this module")

    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        listener_port=dict(type='int', required=True, choices=[i for i in range(1,65536)]),
        state=dict(type='str', required=True, choices=['present', 'absent', 'list', 'stopped', 'running']),
        load_balancer_id=dict(type='str', required=True, aliases=['id']),
        backend_server_port=dict(type='int', required=False, choices=[i for i in range(1,65536)]),
        bandwidth=dict(type='int', required=False, choices=([i for i in range(1,1001)]).append(-1)),
        sticky_session=dict(type='str', required=False, choices=['on', 'off']),
        listener_type=dict(type='str', required=False, choices=['http','https','tcp','udp']),
        health_check=dict(type='str', required=False, choices=['on', 'off']),
        access_control_status=dict(type='str', required=False, choices=['open_white_list', 'close']),
        scheduler=dict(type='str', required=False, default='wrr', choices=['wrr', 'wlc']),
        source_items=dict(type='str', required=False),
        sticky_session_type=dict(type='str', required=False, choices=['insert', 'server']),
        cookie_timeout=dict(type='str', required=False, choices=[i for i in range(1,86401)]),
        cookie=dict(type='str', required=False),
        health_check_domain=dict(type='str', required=False, choices=['$_ip', 'custom string']),
        health_check_uri=dict(type='str', required=False),
        health_check_connect_port=dict(type='int', required=False, choices=([i for i in range(1,65536)]).append(-520)),
        healthy_threshold=dict(type='int', required=False, choices=[i for i in range(1,11)]),
        unhealthy_threshold=dict(type='int', required=False, choices=[i for i in range(1,11)]),
        health_check_timeout=dict(type='int', required=False, choices=[i for i in range(1,51)]),
        health_check_interval=dict(type='int', required=False, choices=[i for i in range(1,6)]),
        health_check_http_code=dict(type='str', required=False),
        vserver_group_id=dict(type='str', required=False),
        gzip=dict(type='str', required=False, default='on', choices=['on', 'off']),
        server_certificate_id=dict(type='str', required=False),
        master_slave_server_group_id=dict(type='str', required=False),
        persistence_timeout=dict(type='int', required=False, default=0, choices=[i for i in range(0,3601)])
    ))

    module = AnsibleModule(argument_spec=argument_spec)
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

    listener = {}
    listener = assemble_request_data(listener, 'load_balancer_id', load_balancer_id)
    listener = assemble_request_data(listener, 'listener_port', listener_port)
    listener = assemble_request_data(listener, 'backend_server_port', backend_server_port)
    listener = assemble_request_data(listener, 'bandwidth', bandwidth)
    listener = assemble_request_data(listener, 'sticky_session', sticky_session)
    listener = assemble_request_data(listener, 'listener_type', listener_type)
    listener = assemble_request_data(listener, 'health_check', health_check)
    listener = assemble_request_data(listener, 'access_control_status', access_control_status)
    listener = assemble_request_data(listener, 'scheduler', scheduler)
    listener = assemble_request_data(listener, 'source_items', source_items)
    listener = assemble_request_data(listener, 'sticky_session_type', sticky_session_type)
    listener = assemble_request_data(listener, 'cookie_timeout', cookie_timeout)
    listener = assemble_request_data(listener, 'cookie', cookie)
    listener = assemble_request_data(listener, 'health_check_domain', health_check_domain)
    listener = assemble_request_data(listener, 'health_check_uri', health_check_uri)
    listener = assemble_request_data(listener, 'health_check_connect_port', health_check_connect_port)
    listener = assemble_request_data(listener, 'healthy_threshold', healthy_threshold)
    listener = assemble_request_data(listener, 'unhealthy_threshold', unhealthy_threshold)
    listener = assemble_request_data(listener, 'health_check_timeout', health_check_timeout)
    listener = assemble_request_data(listener, 'health_check_interval', health_check_interval)
    listener = assemble_request_data(listener, 'health_check_http_code', health_check_http_code)
    listener = assemble_request_data(listener, 'vserver_group_id', vserver_group_id)
    listener = assemble_request_data(listener, 'gzip', gzip)
    listener = assemble_request_data(listener, 'server_certificate_id', server_certificate_id)
    listener = assemble_request_data(listener, 'master_slave_server_group_id', master_slave_server_group_id)
    listener = assemble_request_data(listener, 'persistence_timeout', persistence_timeout)
    
    changed = False
    cur_ls = None
    try:
        cur_ls = slb.describe_load_balancer_listener_attribute(listener)
    except Exception as e:
        cur_ls = None

    if state == "present":
        if cur_ls:
            if access_control_status:
                #set access_control_status
                changed = cur_ls.set_access_control_status(listener)
            elif source_items:
                #add listener_white_list_item
                changed = cur_ls.add_white_list_item(listener)
            else:
                #set attribute
                changed = cur_ls.set_attribute(listener)
            module.exit_json(changed=changed, load_balancer_id = load_balancer_id)
        else:
            changed = slb.create_load_balancer_listener(listener)
            module.exit_json(changed=changed, load_balancer_id = load_balancer_id)
    if not cur_ls:
        module.fail_json(msg="The specified load balancer listener is not exist. Please check your load_balancer_id or listener_port and try again.")
    if state == "absent":
        if source_items:
            #remove listener_white_list_item
            changed = cur_ls.remove_white_list_item(listener)
            module.exit_json(changed=changed, load_balancer_id=load_balancer_id)
        #delete 
        changed = cur_ls.delete(listener)
        module.exit_json(changed=changed, load_balancer_id=load_balancer_id)
    if state == "running":
        #start
        changed = cur_ls.start(listener)
        module.exit_json(changed=changed, load_balancer_id=load_balancer_id)
    if state == "stopped":
        #stop
        changed = cur_ls.stop(listener)
        module.exit_json(changed=changed, load_balancer_id=load_balancer_id)
    if state == 'list':
        #list attribute
        obj = cur_ls.describe_attribute(listener)
        module.exit_json(changed=changed, load_balancer_id=load_balancer_id, listener=get_info(obj))

if __name__ == "__main__":
    main()

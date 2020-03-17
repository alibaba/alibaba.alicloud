#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_dns_domain_info
version_added: "2.9"
short_description: Gather info on dns of Alibaba Cloud.
description:
     - This module fetches data from the Open API in Alicloud.
       The module must be called from within the dns itself.
options:
  domain_name:
    description:
      -  The name to give your DNS.
    required: True
    aliases: ['name']
    type: str
  filters:
    description:
      -  A dict of filters to apply. Each dict item consists of a filter key and a filter value. The filter keys can be
         all of request parameters. 
    type: dict
requirements:
    - "python >= 3.6"
    - "footmark >= 1.15.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Retrieving dns using domain name
  ali_dns_domain_info:
    domain_name: '{{ domain_name }}'

- name: Retrieving all dns
  ali_dns_domain_info:
"""

RETURN = '''
dns:
    description: info about the DNS that was created or deleted
    returned: always
    type: complex
    contains:
        ali_domain:
            description: Whether it is the domain name of Alibaba Cloud.
            returned: always
            type: bool
            sample: false
        dns_servers:
            description: The DNS list of the domain name in the resolution system.
            returned: always
            sample: 
                dns_servers:
                    dns_server: 
                     - xx1.alidns.com
                     - xx2.alidns.com
        domain_name:
            description: The name of domain.
            returned: always
            type: string
            sample: ansiblexxx.abc
        name:
            description: alias of 'domain_name'.
            returned: always
            type: string
            sample: ansiblexxx.abc
        id:
            description: alias of 'domain_id'.
            returned: always
            type: string
            sample: dns-c2e00da5
        puny_code:
            description: Chinese domain name punycode code, English domain name returned empty
            type: bool
            sample: ansiblexxx.abc
        record_count:
            description: The number of parsing records contained in the domain name
            returned: always
            type: int
            sample: 0
        remark:
            description: A comment for dns
            returned: always
            type: string
            sample: ansible_test_dns_domain
        starmark:
            description: Whether to query the domain name star.
            returned: always
            type: bool
            sample: false
        domain_id:
            description: DNS resource id
            returned: always
            type: string
            sample: dns-c2e00da5
        version_code:
            description: Cloud resolution version Code
            returned: always
            type: string
            sample: mianfei
        version_name:
            description: Cloud resolution product name
            returned: always
            type: string
            sample: Alibaba Cloud DNS
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, dns_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import DNSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        domain_name=dict(type='str', aliases=['name']),
        filters=dict(type='dict')
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    filters = module.params['filters']
    if not filters:
        filters = {}
    domain_name = module.params['domain_name']
    try:
        dns = []
        names = []
        for _dns in dns_connect(module).describe_domains(**filters):
            if domain_name and _dns.domain_name != domain_name:
                continue
            dns.append(_dns.read())
            names.append(_dns.domain_name)

        module.exit_json(changed=False, names=names, dns=dns)
    except Exception as e:
        module.fail_json(msg=str("Unable to get dns, error:{0}".format(e)))


if __name__ == '__main__':
    main()

#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

DOCUMENTATION = '''
---
module: ali_security_group
version_added: "2.8"
short_description: Manage Alibaba Cloud Security Group and its rules.
description:
  - Create and Delete Security Group, and it contains security group rules management.
options:
  state:
    description:
      - Create, delete a security group
    default: 'present'
    choices: ['present', 'absent']
  group_name:
    description:
      - Name of the security group, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, "_", "." or "-".
        It cannot begin with http:// or https://.
    aliases: ['name']
  description:
    description:
      - Description of the security group, which is a string of 2 to 256 characters.
      - It cannot begin with http:// or https://.
  vpc_id:
    description:
      - ID of the VPC to which the security group belongs.
  rules:
    description:
      - List of hash/dictionaries firewall inbound rules to enforce in this group (see example). If none are supplied,
        no inbound rules will be enabled. Each rule has several keys and refer to
        https://www.alibabacloud.com/help/doc-detail/25554.htm. Each key should be format as under_score.
        At present, the valid keys including "ip_protocol", "port_range", "source_port_range", "nic_type", "policy",
        "dest_cidr_ip", "source_cidr_ip", "source_group_id", "source_group_owner_account", "source_group_owner_id",
        "priority" and "description".
  rules_egress:
    description:
      - List of hash/dictionaries firewall outbound rules to enforce in this group (see example). If none are supplied,
        no outbound rules will be enabled. Each rule has several keys and refer to
        https://www.alibabacloud.com/help/doc-detail/25560.htm. Each key should be format as under_score.
        At present, the valid keys including "ip_protocol", "port_range", "source_port_range", "nic_type", "policy",
        "dest_cidr_ip", "source_cidr_ip", "dest_group_id", "dest_group_owner_account", "dest_group_owner_id",
        "priority" and "description".
  purge_rules:
    description:
      - Purge existing rules on security group that are not found in rules
    default: True
    type: bool
  purge_rules_egress:
    description:
      - Purge existing rules_egress on security group that are not found in rules_egress
    default: True
    type: bool
  group_id:
    description:
      - Security group ID. It is required when deleting or querying security group or performing rules authorization.
    aliases: ['id']
  tags:
    description:
      - A hash/dictionaries of security group tags. C({"key":"value"})
    aliases: ["group_tags"]
requirements:
    - "python >= 2.6"
    - "footmark >= 1.7.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
'''

EXAMPLES = '''
#
# Provisioning new Security Group
#

# Basic provisioning example to create security group
- name: create security group
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
  tasks:
    - name: create security grp
      ali_security_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_name: 'AliyunSG'

# Basic provisioning example authorize security group
- name: authorize security grp
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
  tasks:
    - name: authorize security group
      ali_security_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        group_id: xxxxxxxxxx
        alicloud_region: '{{ alicloud_region }}'
        rules:
          - ip_protocol: tcp
            port_range: 1/122
            source_cidr_ip: '10.159.6.18/12'
        rules_egress:
          - proto: all
            port_range: -1/-1
            dest_group_id: xxxxxxxxxx
            nic_type: intranet

# Provisioning example create and authorize security group
- name: create and authorize security group
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
  tasks:
    - name: create and authorize security grp
      ali_security_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        group_name: 'AliyunSG'
        description: 'an example ECS group'
        alicloud_region: '{{ alicloud_region }}'
        rules:
          - ip_protocol: tcp
            port_range: 1/122
            source_cidr_ip: '10.159.6.18/12'
            priority: 10
            policy: drop
            nic_type: intranet
        rules_egress:
          - proto: all
            port_range: -1/-1
            dest_group_id: xxxxxxxxxx
            group_owner_id: xxxxxxxxxx
            priority: 10
            policy: accept
            nic_type: intranet

# Provisioning example to delete security group
- name: delete security grp
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: us-west-1
    group_ids:
     - xxxxxxxxxx
    state: absent
  tasks:
    - name: delete security grp
      ali_security_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_ids: '{{ group_ids }}'
        state: '{{ state }}'

'''

RETURN = '''
group:
    description: Dictionary of security group values
    returned: always
    type: complex
    contains:
        description:
            description: The Security Group description.
            returned: always
            type: string
            sample: "my ansible group"
        group_name:
            description: Security group name
            sample: "my-ansible-group"
            type: string
            returned: always
        group_id:
            description: Security group id
            sample: sg-abcd1234
            type: string
            returned: always
        id:
            description: Alias of "group_id".
            sample: sg-abcd1234
            type: string
            returned: always
        inner_access_policy:
            description: Whether can access each other in one security group.
            sample: True
            type: bool
            returned: always
        tags:
            description: Tags associated with the security group
            sample:
            Name: My Security Group
            From: Ansible
            type: dict
            returned: always
        vpc_id:
            description: ID of VPC to which the security group belongs
            sample: vpc-abcd1234
            type: string
            returned: always
        permissions:
            description: Inbound rules associated with the security group.
            sample:
                - create_time: "2018-06-28T08:45:58Z"
                  description: "None"
                  dest_cidr_ip: "None"
                  dest_group_id: "None"
                  dest_group_name: "None"
                  dest_group_owner_account: "None"
                  direction: "ingress"
                  ip_protocol: "TCP"
                  nic_type: "intranet"
                  policy: "Accept"
                  port_range: "22/22"
                  priority: 1
                  source_cidr_ip: "0.0.0.0/0"
                  source_group_id: "None"
                  source_group_name: "None"
                  source_group_owner_account: "None"
            type: list
            returned: always
        permissions_egress:
            description: Outbound rules associated with the security group.
            sample:
                - create_time: "2018-06-28T08:45:59Z"
                  description: "NOne"
                  dest_cidr_ip: "192.168.0.54/32"
                  dest_group_id: "None"
                  dest_group_name: "None"
                  dest_group_owner_account: "None"
                  direction: "egress"
                  ip_protocol: "TCP"
                  nic_type: "intranet"
                  policy: "Accept"
                  port_range: "80/80"
                  priority: 1
                  source_cidr_ip: "None"
                  source_group_id: "None"
                  source_group_name: "None"
                  source_group_owner_account: "None"
            type: list
            returned: always
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect


try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


VALID_INGRESS_PARAMS = ["ip_protocol", "port_range", "source_port_range", "nic_type", "policy",
                        "dest_cidr_ip", "source_cidr_ip", "priority", "description",
                        "source_group_id", "source_group_owner_account", "source_group_owner_id"]
VALID_EGRESS_PARAMS = ["ip_protocol", "port_range", "source_port_range", "nic_type", "policy",
                       "dest_cidr_ip", "source_cidr_ip", "priority", "description",
                       "dest_group_id", "dest_group_owner_account", "dest_group_owner_id"]


def validate_group_rule_keys(module, rule, direction):

    if not isinstance(rule, dict):
        module.fail_json(msg='Invalid rule parameter type [{0}].'.format(type(rule)))

    VALID_PARAMS = VALID_INGRESS_PARAMS
    if direction == "egress":
        VALID_PARAMS = VALID_EGRESS_PARAMS

    for k in rule:
        if k not in VALID_PARAMS:
            module.fail_json(msg="Invalid rule parameter '{0}' for rule: {1}. Supported parametes include: {2}".format(k, rule, VALID_PARAMS))

    if 'ip_protocol' not in rule:
        module.fail_json(msg='ip_protocol is required.')
    if 'port_range' not in rule:
        module.fail_json(msg='port_range is required.')
    # The system response will return upper protocol
    rule['ip_protocol'] = str(rule['ip_protocol']).upper()


def purge_rules(module, group, existing_rule, rules, direction):

    if not isinstance(existing_rule, dict):
        module.fail_json(msg='Invalid existing rule type [{0}].'.format(type(existing_rule)))

    if not isinstance(rules, list):
        module.fail_json(msg='Invalid rules type [{0}]. The specified rules should be a list.'.format(type(rules)))

    VALID_PARAMS = VALID_INGRESS_PARAMS
    if direction == "egress":
        VALID_PARAMS = VALID_EGRESS_PARAMS

    # Find the rules which is not in the specified rules
    find = False
    for rule in rules:
        for key in VALID_PARAMS:
            if not rule.get(key):
                continue
            if existing_rule.get(key) != rule.get(key):
                find = False
                break
            find = True
        if find:
            break
    # If it is not found, there will not purge anythind
    if not find:
        return group.revoke(existing_rule, direction)
    return False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', type='str', choices=['present', 'absent']),
        group_name=dict(type='str', required=False, aliases=['name']),
        description=dict(type='str', required=False),
        vpc_id=dict(type='str'),
        tags=dict(type='dict', aliases=['group_tags']),
        rules=dict(type='list'),
        rules_egress=dict(type='list'),
        purge_rules=dict(type='bool', default=True),
        purge_rules_egress=dict(type='bool', default=True),
        group_id=dict(type='str', aliases=['id'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark is required for the module ali_security_group.')

    ecs = ecs_connect(module)

    state = module.params['state']
    group_name = module.params['group_name']
    group_id = module.params['group_id']

    changed = False
    group = None

    try:
        if group_id:
            group = ecs.describe_security_group_attribute(security_group_id=group_id)
    except ECSResponseError as e:
        module.fail_json(msg='Faild to describe security group {0}: {1}'.format(group_id, e))

    if state == 'absent':
        if not group:
            module.exit_json(changed=changed, group={})
        try:
            module.exit_json(changed=group.delete(), group={})
        except ECSResponseError as e:
            module.fail_json(msg="Deleting security group {0} is failed. Error: {1}".format(group.id, e))

    if not group:
        try:
            params = module.params
            params['security_group_name'] = group_name
            params['client_token'] = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
            group = ecs.create_security_group(**params)
            changed = True
        except ECSResponseError as e:
            module.fail_json(changed=changed, msg='Creating a security group is failed. Error: {0}'.format(e))

    if not group_name:
        group_name = group.security_group_name

    description = module.params['description']
    if not description:
        description = group.description
    if group.modify(name=group_name, description=description):
        changed = True

    # validating rules if provided
    ingress_rules = module.params['rules']
    if ingress_rules:
        direction = 'ingress'
        for rule in ingress_rules:
            validate_group_rule_keys(module, rule, direction)
        if module.params['purge_rules']:
            for existing in group.permissions:
                if existing['direction'] != direction:
                    continue
                if purge_rules(module, group, existing, ingress_rules, direction):
                    changed = True
        for rule in ingress_rules:
            if group.authorize(rule, direction):
                changed = True

    egress_rules = module.params['rules_egress']
    if egress_rules:
        direction = 'egress'
        for rule in egress_rules:
            validate_group_rule_keys(module, rule, direction)
        if module.params['purge_rules_egress']:
            for existing in group.permissions:
                if existing['direction'] != direction:
                    continue
                if purge_rules(module, group, existing, egress_rules, direction):
                    changed = True
        for rule in egress_rules:
            if group.authorize(rule, direction):
                changed = True

    module.exit_json(changed=changed, group=group.get().read())


if __name__ == '__main__':
    main()

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_security_group
version_added: "2.5"
short_description: Create, Query or Delete Security Group.
description:
  - Create, Query or Delete Security Group, and it contains security group rules management.
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
      - List of hash/dictionaries firewall inbound rules to enforce in this group.
    suboptions:
        ip_protocol:
          description:
            - IP protocol
          required: true
          choices: ["tcp", "udp", "icmp", "gre", "all"]
          aliases: ['proto']
        port_range:
          description:
            - The range of port numbers. Tcp and udp's valid range is 1 to 65535, and other protocol's valid value is -1/-1.
          required: true
        source_group_id:
          description:
            - The source security group id.
          aliases: ['group_id']
        source_group_owner_id:
          description:
            - The source security group owner id.
          aliases: ['group_owner_id']
        source_cidr_ip:
          description:
            - The source IP address range
          aliases: ['cidr_ip']
        policy:
          description:
            - Authorization policy
          default: "accept"
          choices: ["accept", "drop"]
        priority:
          description:
            - Authorization policy priority
          default: 1
          choices: ["1~100"]
        nic_type:
          description:
            - Network type
          default: "internet"
          choices: ["internet", "intranet"]
  rules_egress:
    description:
      - List of hash/dictionaries firewall outbound rules to enforce in this group.
        Keys allowed are:ip_protocol, port_range, dest_group_id, dest_group_owner_id, dest_cidr_ip, policy, priority,nic_type.
        And these keys's attribution same as rules keys.
    suboptions:
        ip_protocol:
          description:
            - IP protocol
          required: true
          choices: ["tcp", "udp", "icmp", "gre", "all"]
          aliases: ['proto']
        port_range:
          description:
            - The range of port numbers. Tcp and udp's valid range is 1 to 65535, and other protocol's valid value is "-1/-1".
          required: true
        dest_group_id:
          description:
            - The destination security group id.
          aliases: ['group_id']
        dest_group_owner_id:
          description:
            - The destination security group owner id.
          aliases: ['group_owner_id']
        dest_cidr_ip:
          description:
            - The destination IP address range
          aliases: ['cidr_ip']
        policy:
          description:
            - Authorization policy
          default: "accept"
          choices: ["accept", "drop"]
        priority:
          description:
            - Authorization policy priority
          default: 1
          choices: ["1~100"]
        nic_type:
          description:
            - Network type
          default: "internet"
          choices: ["internet", "intranet"]
  group_id:
    description:
      - Security group ID. It is required when deleting or querying security group or performing rules authorization.
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
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
      alicloud_security_group:
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
      alicloud_security_group:
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
      alicloud_security_group:
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
      alicloud_security_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        group_ids: '{{ group_ids }}'
        state: '{{ state }}'


# Provisioning example to querying security group list
- name: querying security group list
  hosts: localhost
  connection: local
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    state: list
  tasks:
    - name: Querying Security group list
      alicloud_security_group:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        state: '{{ state }}'
'''

RETURN = '''
group_id:
    description: security group ID
    returned: when present and absent
    type: string
    sample: "sd-safhi3gsv"
group_ids:
    description: list IDs of security groups
    returned: when list
    type: list
    sample: ["sg-3de1hhyn7tac4p85gh23", "sg-2ze1hhyn7tac4p85gh45"]
group:
    description: Details about the security group that was created
    returned: when present
    type: dict
    sample: {
        "description": "travis-ansible-instance",
        "id": "sg-2ze1hhyn7tac4p85gh13",
        "name": "travis-ansible-instance",
        "region_id": "cn-beijing",
        "rules": [
            {
                "create_time": "2017-06-19T02:43:29Z",
                "description": "",
                "dest_cidr_ip": "",
                "dest_group_id": "",
                "dest_group_name": "",
                "dest_group_owner_account": "",
                "direction": "ingress",
                "ip_protocol": "TCP",
                "nic_type": "internet",
                "policy": "Accept",
                "port_range": "80/86",
                "priority": 1,
                "source_cidr_ip": "192.168.0.54/32",
                "source_group_id": "",
                "source_group_name": "",
                "source_group_owner_account": ""
            },
            {
                "create_time": "2017-06-19T02:43:30Z",
                "description": "",
                "dest_cidr_ip": "47.89.23.33/32",
                "dest_group_id": "",
                "dest_group_name": "",
                "dest_group_owner_account": "",
                "direction": "egress",
                "ip_protocol": "TCP",
                "nic_type": "internet",
                "policy": "Accept",
                "port_range": "8080/8085",
                "priority": 1,
                "source_cidr_ip": "",
                "source_group_id": "",
                "source_group_name": "",
                "source_group_owner_account": ""
            }
        ],
        "tags": {},
        "vpc_id": ""
    }
groups:
    description: Details about the security group that was created
    returned: when list
    type: list
    sample: [
        {
            "description": "travis-ansible-instance",
            "id": "sg-2ze1hhyn7tac4p85gh13",
            "name": "travis-ansible-instance",
            "region_id": "cn-beijing",
            "rules": [
                {
                    "create_time": "2017-06-19T02:43:29Z",
                    "description": "",
                    "dest_cidr_ip": "",
                    "dest_group_id": "",
                    "dest_group_name": "",
                    "dest_group_owner_account": "",
                    "direction": "ingress",
                    "ip_protocol": "TCP",
                    "nic_type": "internet",
                    "policy": "Accept",
                    "port_range": "80/86",
                    "priority": 1,
                    "source_cidr_ip": "192.168.0.54/32",
                    "source_group_id": "",
                    "source_group_name": "",
                    "source_group_owner_account": ""
                },
                {
                    "create_time": "2017-06-19T02:43:30Z",
                    "description": "",
                    "dest_cidr_ip": "47.89.23.33/32",
                    "dest_group_id": "",
                    "dest_group_name": "",
                    "dest_group_owner_account": "",
                    "direction": "egress",
                    "ip_protocol": "TCP",
                    "nic_type": "internet",
                    "policy": "Accept",
                    "port_range": "8080/8085",
                    "priority": 1,
                    "source_cidr_ip": "",
                    "source_group_id": "",
                    "source_group_name": "",
                    "source_group_owner_account": ""
                }
            ],
            "tags": {},
            "vpc_id": ""
        }
    ]
vpc_id:
    description: ID of the VPC to which the security group belongs
    returned: when present
    type: string
    sample: "vpc-snif3g3iv"
vpc_ids:
    description: list IDs of the VPC to which the list security groups belong
    returned: when list
    type: list
    sample: ["vpc-12snif3g3iv", "vpc-s324vif3g3iv"]
total:
    description: The number of all security groups after list.
    returned: when list
    type: int
    sample: 3
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect


try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def authorize_security_group(module, ecs, group_id, inbound_rules, outbound_rules):
    """
    authorize security group in ecs
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param group_id: Security Group Id for authorization
    :param inbound_rules: Inbound rules for authorization
    :param outbound_rules: Outbound rules for authorization
    :param add_to_fail_result: message to add to failed message at the beginning, if two tasks are performed
    :return: Returns changed state, security group id and custom message.
    """

    try:
        changed = False
        inbound_failed_rules, outbound_failed_rules, result = ecs.authorize_security_group(
            group_id, inbound_rules, outbound_rules)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg="Authorizing SecurityGroup is failed, error: %s ; group_id: %s ; "
                                                  "failed inbound rules: %s ; failed outbound rules: %s."
                                                  % (str(result), group_id, inbound_failed_rules, outbound_failed_rules))
        changed = True

    except ECSResponseError as e:
        module.fail_json(msg='Unable to authorize security group, error: {0}'.format(e))

    return changed


def validate_format_sg_rules(module, inbound_rules=None, outbound_rules=None):
    """
    Validate and format security group for inbound and outbound rules
    :param module: Ansible module object
    :param inbound_rules: Inbound rules for authorization to validate and format
    :param outbound_rules: Outbound rules for authorization to validate and format
    :return:
    """
    # aliases for rule
    ip_protocol_aliases = ('ip_protocol', 'proto')
    inbound_cidr_ip_aliases = ('source_cidr_ip', 'cidr_ip')
    outbound_cidr_ip_aliases = ('dest_cidr_ip', 'cidr_ip')
    inbound_group_id_aliases = ('source_group_id', 'group_id')
    outbound_group_id_aliases = ('dest_group_id', 'group_id')
    inbound_group_owner_aliases = ('source_group_owner_id', 'group_owner_id')
    outbound_group_owner_aliases = ('dest_group_owner_id', 'group_owner_id')

    cidr_ip_aliases = {
        "inbound": inbound_cidr_ip_aliases,
        "outbound": outbound_cidr_ip_aliases,
    }

    group_id_aliases = {
        "inbound": inbound_group_id_aliases,
        "outbound": outbound_group_id_aliases,
    }

    group_owner_aliases = {
        "inbound": inbound_group_owner_aliases,
        "outbound": outbound_group_owner_aliases,
    }

    COMMON_VALID_PARAMS = ('proto', 'ip_protocol', 'cidr_ip', 'group_id', 'group_owner_id',
                           'nic_type', 'policy', 'priority', 'port_range')
    INBOUND_VALID_PARAMS = ('source_cidr_ip', 'source_group_id', 'source_group_owner_id')
    OUTBOUND_VALID_PARAMS = ('dest_cidr_ip', 'dest_group_id', 'dest_group_owner_id')

    rule_types = []

    rule_choice = {
        "inbound": inbound_rules,
        "outbound": outbound_rules,
    }
    valid_params = {
        "inbound": INBOUND_VALID_PARAMS,
        "outbound": OUTBOUND_VALID_PARAMS,
    }

    if inbound_rules:
        rule_types.append('inbound')

    if outbound_rules:
        rule_types.append('outbound')

    for rule_type in rule_types:

        rules = rule_choice.get(rule_type)
        total_rules = 0
        if rules:
            total_rules = len(rules)

        if total_rules != 0:

            for rule in rules:

                if not isinstance(rule, dict):
                    module.fail_json(msg='Invalid rule parameter type [%s].' % type(rule))

                for k in rule:
                    if k not in COMMON_VALID_PARAMS and k not in valid_params.get(rule_type):
                        module.fail_json(msg='Invalid rule parameter \'{}\''.format(k))

                ip_protocol = get_alias_value(rule, ip_protocol_aliases)
                if ip_protocol is None:
                    module.fail_json(msg="Ip Protocol required for rule authorization")

                port_range = get_alias_value(rule, ['port_range'])
                if port_range is None:
                    module.fail_json(msg="Port range is required for rule authorization")

                # verifying whether group_id is provided and cidr_ip is not, so nic_type should be set to intranet
                cidr_ip = get_alias_value(rule, cidr_ip_aliases.get(rule_type))
                if cidr_ip is None:
                    if get_alias_value(rule, group_id_aliases.get(rule_type)) is not None:
                        if 'nic_type' in rule:
                            if not rule['nic_type'] == "intranet":
                                module.fail_json(msg="In mutual security group authorization (namely, "
                                                     "GroupId is specified, while CidrIp is not specified), "
                                                     "you must specify the nic_type as intranet")
                        else:
                            module.fail_json(msg="In mutual security group authorization (namely, "
                                                 "GroupId is specified, while CidrIp is not specified), "
                                                 "you must specify the nic_type as intranet")

                # format rules to return for authorization
                formatted_rule = {}

                formatted_rule['ip_protocol'] = ip_protocol
                formatted_rule['port_range'] = port_range

                if cidr_ip:
                    formatted_rule['cidr_ip'] = cidr_ip

                group_id = get_alias_value(rule, group_id_aliases.get(rule_type))
                if group_id:
                    formatted_rule['group_id'] = group_id

                group_owner_id = get_alias_value(rule, group_owner_aliases.get(rule_type))
                if group_owner_id:
                    formatted_rule['group_owner_id'] = group_owner_id

                if 'nic_type' in rule:
                    if rule['nic_type']:
                        formatted_rule['nic_type'] = rule['nic_type']

                if 'policy' in rule:
                    if rule['policy']:
                        formatted_rule['policy'] = rule['policy']

                if 'priority' in rule:
                    if rule['priority']:
                        formatted_rule['priority'] = rule['priority']

                rule.clear()
                rule.update(formatted_rule)


def get_alias_value(dictionary, aliases):
    """
    Get alias or key value from a dictionary
    :param dictionary: a dictionary to check in for keys/aliases
    :param aliases: list of aliases to find in dictionary to retrieve value
    :return: returns value of found alias else None
    """

    if (dictionary and aliases) is not None:
        for alias in aliases:
            if alias in dictionary:
                return dictionary[alias]
        return None
    else:
        return None


def get_group_basic(group):
    """
    Parse security group basic information.
    returns it as a dictionary
    """
    return {'id': group.id, 'name': group.name, 'vpc_id': group.vpc_id}


def get_group_detail(group):
    """
    Parse security group detail information.
    returns it as a dictionary
    """
    return {'id': group.id, 'name': group.name, 'description': group.description, 'region_id': group.region_id,
            'tags': group.tags, 'vpc_id': group.vpc_id, 'rules': group.rules}


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', type='str', choices=['present', 'absent']),
        group_name=dict(type='str', required=False, aliases=['name']),
        description=dict(type='str', required=False),
        vpc_id=dict(type='str'),
        group_tags=dict(type='list', aliases=['tags']),
        rules=dict(type='list'),
        rules_egress=dict(type='list'),
        group_id=dict(type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_security_group.')

    ecs = ecs_connect(module)

    state = module.params['state']
    group_name = module.params['group_name']
    description = module.params['description']
    vpc_id = module.params['vpc_id']
    group_id = module.params['group_id']
    group_tags = module.params['group_tags']

    changed = False
    group = None
    groups_by_name = []

    try:
        if group_id:
            security_groups = ecs.get_all_security_groups(group_ids=[group_id], vpc_id=vpc_id)
        else:
            security_groups = ecs.get_all_security_groups(vpc_id=vpc_id)
    except ECSResponseError as e:
        module.fail_json(msg='Error in get_all_security_groups: %s' % str(e))

    if security_groups and len(security_groups) == 1:
        group = security_groups[0]

    group_ids_by_name = []
    group_ids = []
    if not group and group_name and security_groups:
        for cur in security_groups:
            if cur.name == group_name:
                group_ids_by_name.append(cur.id)
                groups_by_name.append(cur)

            group_ids.append(cur.id)

        if len(groups_by_name) == 1:
            group = groups_by_name[0]
        elif len(groups_by_name) > 1:
            module.fail_json(msg="There is too many security groups match name '{0}', "
                                 "please use group_id or a new group_name and vpc_id to specify a unique group."
                                 "Matched group ids are: {1}".format(group_name, group_ids_by_name))

    if state == 'absent':
        if group:
            try:
                changed = group.delete()
                module.exit_json(changed=changed)
            except ECSResponseError as e:
                module.fail_json(msg="Deleting security group {0} is failed. Error: {1}".format(group.id, e))

        module.fail_json(changed=changed, msg="Please specify a security group by using 'group_id' or 'group_name' "
                                              "and 'vpc_id', and expected group ids: {0}".format(group_ids))

    if not group:
        try:
            client_token = "Ansible-Alicloud-%s-%s" % (hash(str(module.params)), str(time.time()))
            group = ecs.create_security_group(group_name=group_name, description=description, vpc_id=vpc_id,
                                              group_tags=group_tags, client_token=client_token)
            changed = True

        except ECSResponseError as e:
            module.fail_json(changed=changed, msg='Creating a security group is failed. Error: {0}'.format(e))

    # validating rules if provided
    total_rules_count = 0
    inbound_rules = module.params['rules']
    if inbound_rules:
        total_rules_count = len(inbound_rules)

    outbound_rules = module.params['rules_egress']
    if outbound_rules:
        total_rules_count += len(outbound_rules)

    if total_rules_count > 100:
        module.fail_json(msg='more than 100 rules for authorization are not allowed')

    validate_format_sg_rules(module, inbound_rules, outbound_rules)

    if inbound_rules or outbound_rules:
        changed = authorize_security_group(module, ecs, group_id=group.id, inbound_rules=inbound_rules, outbound_rules=outbound_rules)

    module.exit_json(changed=changed, group_id=group.id, group=get_group_detail(group), vpc_id=group.vpc_id)


if __name__ == '__main__':
    main()

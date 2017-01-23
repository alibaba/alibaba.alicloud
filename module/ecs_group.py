#!/usr/bin/python

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

from __builtin__ import isinstance

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: ecs_group
short_description: maintain an ecs VPC security group.
description:
    - maintains ecs security groups.

common options:
  acs_access_key:
    description: The access key.
    required: false
    default: null
    aliases: []
  acs_secret_access_key:
    description: The access secret key.
    required: false
    default: null
    aliases: []
  state:
    description: Create or delete a security group
    required: false
    default: present
    choices: [ "present", "absent", "getinfo" ]
  region:
    description: The Alicloud region ID to use for the instance.
    required: true
    default: null
    aliases: [ 'acs_region', 'ecs_region' ]

function create VPC group:
  name:
    description:
      - Name of the security group.
    required: true
  description:
    description:
      - Description of the security group.
    required: false
  vpc_id:
    description:
      - ID of the VPC to create the group in.
    required: false
  group_id:
  description:
    - ID of the security group to authorize.
  required: false
  rules:
    description:
      - List of firewall inbound rules to enforce in this group. If none are supplied, a default all-out rule is assumed.
      If an empty list is supplied, no inbound rules will be enabled.
        Each rule contains four attribute as follows:
        - proto
            description: IP protocal
            choices: ["tcp", "udp", "icmp", "gre", "all"]
            required: true
        - from_port
            description: start port
            choices: depends on proto
            required: true
        - to_port
            description: end port
            choices: depends on proto
            required: true
        - cidr_ip
            description: The IP address range based on CIDR.
            required: false
            default: 0.0.0.0/0
    required: false
  rules_egress:
    description:
      - List of firewall outbound rules to enforce in this group. If none are supplied, a default all-out rule is assumed. If an empty list is supplied, no outbound rules will be enabled.
        Each rule attributes (see rules)
    required: false
  group_tags:
      description: - A list of hash/dictionaries of instance tags, '[{tag_key:"value", tag_value:"value"}]', tag_key must be not null when tag_value isn't null
      required: false
      default: null
      aliases: []

function delete a security group:
  group_ids:
    description:
      - List of the security groups to delete.
    required: true
    default: false
    aliases: [security_group_ids]

function get security groups:
  group_id:
    description:
      - Name of the security group.
    required: true
    default: false
    aliases: [security_group_ids]
  vpc_id:
    description:
      - The ID of the VPC to which the security group belongs.
    required: false
    default: false
'''

# TODO: Add Examples here
EXAMPLES = '''
- name: example ecs group
  ecs_group:
    name: example
    description: an example EC2 group
    vpc_id: 12345
    region: eu-west-1a
    acs_secret_access_key: SECRET
    acs_access_key: ACCESS
    rules:
      - proto: tcp
        from_port: 80
        to_port: 80
        cidr_ip: 0.0.0.0/0
      - proto: tcp
        from_port: 22
        to_port: 22
        cidr_ip: 10.0.0.0/8
      - proto: tcp
        from_port: 443
        to_port: 443
        group_id: amazon-elb/sg-87654321/amazon-elb-sg
      - proto: tcp
        from_port: 3306
        to_port: 3306
        group_id: 123412341234/sg-87654321/exact-name-of-sg
      - proto: udp
        from_port: 10050
        to_port: 10050
        cidr_ip: 10.0.0.0/8
      - proto: udp
        from_port: 10051
        to_port: 10051
        group_id: sg-12345678
      - proto: icmp
        from_port: 8 # icmp type, -1 = any type
        to_port:  -1 # icmp subtype, -1 = any subtype
        cidr_ip: 10.0.0.0/8
      - proto: all
        # the containing group name may be specified here
        group_name: example
    rules_egress:
      - proto: tcp
        from_port: 80
        to_port: 80
        cidr_ip: 0.0.0.0/0
        group_name: example-other
        # description to use if example-other needs to be created
        group_desc: other example EC2 group
'''

# import module snippets
from ansible.module_utils.basic import *

import sys

try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False

try:
    from ecsutils.ecs import *

    HAS_ECS = True
except ImportError:
    HAS_ECS = False


def create_security_group(module, ecs, group_name, group_description, vpc_id, group_tags):
    """
    create and authorize security group in ecs

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param group_name: Name of the security group
    :param group_description: Description of the security group
    :param vpc_id: ID of a vpc to which an security group belongs.
    :param group_tags:  A list of hash/dictionaries of group
            tags, '[{tag_key:"value", tag_value:"value"}]', tag_key
            must be not null when tag_value isn't null

    :return: Returns a dictionary of group information about
            the the group created/authorized. If the group was not
            created and authorized, "changed" will be set to False.
    """

    try:
        changed = False
        changed, security_group_id, result = ecs.create_security_group(group_name=group_name,
                                                                       group_description=group_description,
                                                                       vpc_id=vpc_id,
                                                                       group_tags=group_tags)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, security_group_id=security_group_id, msg=result)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to create and authorize security group, error: {0}'.format(e))

    return changed, security_group_id, result


def authorize_security_group(module, ecs, security_group_id=None, inbound_rules=None, outbound_rules=None,
                             add_to_fail_result=""):
    """

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param security_group_id: Security Group Id for authorization
    :param inbound_rules: Inbound rules for authorization
    :param outbound_rules: Outbound rules for authorization
    :param add_to_fail_result: Outbound rules for authorization
    :return: returns the list of failures if any else returns the successful message
    """
    inbound_failed_rules = None
    outbound_failed_rules = None
    try:
        changed = False

        changed, inbound_failed_rules, outbound_failed_rules, result = ecs.authorize_security_group(
            security_group_id=security_group_id, inbound_rules=inbound_rules,
            outbound_rules=outbound_rules)

        if 'error' in (''.join(str(result))).lower():
            result.insert(0, add_to_fail_result)
            module.fail_json(changed=changed, group_id=security_group_id, msg=result,
                             inbound_failed_rules=inbound_failed_rules, outbound_failed_rules=outbound_failed_rules)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to authorize security group, error: {0}'.format(e))

    return changed, security_group_id, result


def validate_sg_rules(module, inbound_rules=None, outbound_rules=None):
    """

    :param module:
    :param inbound_rules:
    :param outbound_rules:
    :return:
    """
    # aliases for rule
    ip_protocol_aliases = ('proto', 'ip_protocol')
    inbound_cidr_ip_aliases = ('source_cidr_ip', 'cidr_ip')
    outbound_cidr_ip_aliases = ('dest_cidr_ip', 'cidr_ip')
    inbound_group_id_aliases = ('source_group_id', 'group_id')
    outbound_group_id_aliases = ('dest_group_id', 'group_id')

    cidr_ip_aliases = {
        "inbound": inbound_cidr_ip_aliases,
        "outbound": outbound_cidr_ip_aliases,
    }

    group_id_aliases = {
        "inbound": inbound_group_id_aliases,
        "outbound": outbound_group_id_aliases,
    }

    COMMON_VALID_PARAMS = ('proto', 'ip_protocol', 'cidr_ip', 'group_id', 'group_owner_id',
                           'nic_type', 'policy', 'priority', 'port_range')
    INBOUND_VALID_PARAMS = ('source_cidr_ip', 'source_group_id', 'source_group_owner_id')
    OUTBOUND_VALID_PARAMS = ('dest_cidr_ip', 'dest_group_id', 'dest_group_owner_id')

    # tcp_proto_start_port = 1
    # tcp_proto_end_port = 65535

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

                if get_alias_value(rule, ip_protocol_aliases) is None:
                    module.fail_json(msg="Ip Protocol required for rule authorization")

                if get_alias_value(rule, ['port_range']) is None:
                    module.fail_json(msg="Port range is required for rule authorization")

                # verifying whether group_id is provided and cidr_ip is not, so nic_type should be set to intranet
                if get_alias_value(rule, cidr_ip_aliases.get(rule_type)) is None:
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


def get_alias_value(dictionay, aliases):
    """

    :param dictionay: a dictionary to check in for keys
    :param param:
    :param aliases:
    :return:
    """

    if (dictionay and aliases) is not None:
        for alias in aliases:
            if alias in dictionay:
                return dictionay[alias]
        return None
    else:
        return None


def get_security_status(module, ecs, vpc_id=None, group_ids=None):
    """
    Querying Security Group List returns the basic information about all user-defined security groups.

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param vpc_id: ID of a vpc to which an security group belongs. If it is
            null, a vpc is selected by the system
    :param group_ids: Provides a list of security groups ids.
    :return: A list of the total number of security groups,
                 the ID of the VPC to which the security group belongs
    """

    try:
        changed = False
        changed, result = ecs.get_security_status(vpc_id=vpc_id, group_ids=group_ids)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)
        changed = True
    except ECSResponseError as e:
        module.fail_json(msg='Unable to get status of SecurityGroup(s), error: {0}'.format(e))
    return changed, result


def del_security_group(module, ecs, security_group_ids):
    """
    Delete Security Group , delete security group inside particular region.

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param security_group_ids: The Security Group ID

    :return: result of after successfully deletion of security group
    """
    changed = False
    try:
        changed, result = ecs.delete_security_group(group_ids=security_group_ids)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to create instance due to following error :{0}'.format(e))
    return changed, result


def main():
    if HAS_ECS is False:
        print("ecsutils required for this module")
        sys.exit(1)
    elif HAS_FOOTMARK is False:
        print("Footmark required for this module")
        sys.exit(1)

    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        status=dict(default='present', aliases=['state'], choices=['present', 'absent', 'getinfo'], type='str'),
        security_group_name=dict(type='str', aliases=['name']),
        description=dict(type='str'),
        vpc_id=dict(type='str'),
        group_tags=dict(type='list'),
        rules=dict(type='list'),
        rules_egress=dict(type='list'),
        group_ids=dict(type='list', aliases=['security_group_ids', 'group_id', 'security_group_id'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    ecs = ecs_connect(module)

    region, acs_connect_kwargs = get_acs_connection_info(module)

    tagged_instances = []

    state = module.params['status']

    if state == 'present':

        group_name = module.params['security_group_name']
        group_description = module.params['description']
        vpc_id = module.params['vpc_id']
        group_tags = module.params['group_tags']
        group_ids = module.params['group_ids']

        # validating group_id and name
        if group_ids and group_name:
            module.fail_json(msg='provide either security group id or name, not both')
        elif group_ids:
            if len(group_ids) != 1:
                module.fail_json(msg='provide single security group id for rule authorization')
        elif group_name is None:
            module.fail_json(msg='provide either security group id or name')

        # validating rules if provided
        total_rules_count = 0
        inbound_rules = module.params['rules']
        if inbound_rules:
            total_rules_count = len(inbound_rules)

        outbound_rules = module.params['rules_egress']
        if outbound_rules:
            total_rules_count += len(outbound_rules)

        validate_sg_rules(module, inbound_rules, outbound_rules)

        if total_rules_count > 100:
            module.fail_json(msg='more than 100 rules for authorization are not allowed')

        # Verifying if rules are provided for group_id to authorize security group
        if group_ids:
            if total_rules_count == 0:
                module.fail_json(msg='provide rules for authorization')

            changed, security_group_id, result = authorize_security_group(module, ecs, security_group_id=group_ids[0],
                                                                          inbound_rules=inbound_rules,
                                                                          outbound_rules=outbound_rules)
        # if security group creation is required
        else:

            changed, security_group_id, result = create_security_group(module, ecs, group_name=group_name,
                                                                       group_description=group_description,
                                                                       vpc_id=vpc_id,
                                                                       group_tags=group_tags)

            # if rule authorization is required after group creation
            if security_group_id and (inbound_rules or outbound_rules):
                c, s, result_details = authorize_security_group(module, ecs, security_group_id, inbound_rules,
                                                                outbound_rules,
                                                                add_to_fail_result=result[0])
                result.extend(result_details)

        module.exit_json(changed=changed, group_id=security_group_id, msg=result)

    elif state == 'getinfo':
        vpc_id = module.params['vpc_id']
        group_ids = module.params['group_ids']

        (changed, result) = get_security_status(module, ecs, vpc_id, group_ids)
        module.exit_json(changed=changed, result=result)

    elif state == 'absent':

        security_group_ids = module.params['group_ids']

        if not security_group_ids:
            module.fail_json(msg='Security Group Id  is required to Delete from security group')
        else:
            for id in security_group_ids:
                if not id:
                    module.fail_json(msg='Security Group Id  is required to Delete from security group')

        (changed, result) = del_security_group(module, ecs, security_group_ids)
        module.exit_json(changed=changed, result=result)


# import ECSConnection
main()
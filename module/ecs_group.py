#!/usr/bin/python

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
  rules:
    description:
      - List of firewall inbound rules to enforce in this group. If none are supplied, a default all-out rule is assumed. If an empty list is supplied, no inbound rules will be enabled.
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
  group_ids:
    description:
      - List of the security groups .
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


def create_security_group(module, ecs, group_name, group_description, vpc_id, group_tags, inbound_rules,
                          outbound_rules):
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
    :param inbound_rules: Inbound rules for authorization
    :param outbound_rules: Outbound rules for authorization

    :return: Returns a dictionary of group information about
            the the group created/authorized. If the group was not
            created and authorized, "changed" will be set to False.
    """

    try:
        changed = False
        changed, security_group_id, result = ecs.create_security_group(group_name=group_name,
                                                                       group_description=group_description,
                                                                       vpc_id=vpc_id,
                                                                       group_tags=group_tags,
                                                                       inbound_rules=inbound_rules,
                                                                       outbound_rules=outbound_rules)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, security_group_id=security_group_id, msg=result)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to create and authorize security group, error: {0}'.format(e))

    return changed, security_group_id, result


def validate_sg_rules(rules):
    """
    Validating Security Groups

    :param rules: List of rules to validate

    :return: true or false indicating provided rules are valid or invalid. Also Returns the error or success message
    """

    tcp_proto_start_port = 1
    tcp_proto_end_port = 65535

    for rule in rules:

        if 'proto' in rule:
            ip_prototype = rule['proto']

            if ip_prototype in ("tcp", "udp"):

                if 'from_port' in rule:
                    from_port = int(rule['from_port'])
                else:
                    from_port = tcp_proto_start_port

                if 'to_port' in rule:
                    to_port = int(rule['to_port'])
                else:
                    to_port = tcp_proto_end_port

                if not from_port <= to_port and from_port >= tcp_proto_start_port and to_port <= tcp_proto_end_port:
                    return False, "For protocol tcp or udp, port range is 1-65535"

            elif ip_prototype not in ('icmp', 'gre', 'all'):
                return False, ip_prototype + " is not a valid protocol"

            if 'group_id' in rule:
                if 'cidr_ip' not in rule:
                    if 'nic_type' in rule:
                        if 'intranet' not in rule['nic_type']:
                            return False, """In mutual security group authorization (namely, SourceGroupId is specified,
                                          while SourceCidrIp is not specified), you must specify the NicType
                                          as intranet"""
                    else:
                        return False, """In mutual security group authorization (namely, SourceGroupId is specified,
                                                                  while SourceCidrIp is not specified), you must
                                                                  specify the NicType as intranet"""
            elif 'cidr_ip' not in rule:
                return False, "Either the SourceGroupId or SourceCidrIp parameter must be set"

            if 'policy' in rule:
                if rule['policy'] not in ('accept', 'drop'):
                    return False, rule['policy'] + " is not a valid policy parameter"

            if 'priority' in rule:
                priority = int(rule['priority'])
                if priority < 1 or priority > 100:
                    return False, rule['priority'] + " is not a valid priority parameter"

            if 'nic_type' in rule:
                if rule['nic_type'] not in ('intranet', 'internet'):
                    return False, rule['nic_type'] + " is not a valid NicType parameter"


        else:
            return False, "Prototype is mandatory for authorization"

    return True, "Validation Successful"


def get_security_status(module, ecs, vpc_id=None, group_id=None):
    """
    Querying Security Group List returns the basic information about all user-defined security groups.

    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param vpc_id: ID of a vpc to which an security group belongs. If it is
            null, a vpc is selected by the system
    :param group_id: Provides a list of security groups ids.
    :return: A list of the total number of security groups,
                 the ID of the VPC to which the security group belongs
    """

    try:
        changed = False
        changed, result = ecs.get_security_status(vpc_id=vpc_id, group_id=group_id)

        if 'error:' in (''.join(result)).lower():
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
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent', 'getinfo'], type='str'),
        name=dict(type='str'),
        description=dict(type='str'),
        vpc_id=dict(type='str'),
        group_id=dict(),
        group_tags=dict(type='list'),
        rules=dict(type='list'),
        rules_egress=dict(type='list'),
        group_ids=dict(type='list'),
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_ECS:
        module.fail_json(msg='ecsutils and footmark required for this module')

    ecs = ecs_connect(module)

    region, acs_connect_kwargs = get_acs_connection_info(module)

    tagged_instances = []

    state = module.params['state']

    if state == 'present':

        group_name = module.params['name']
        group_description = module.params['description']
        vpc_id = module.params['vpc_id']
        group_tags = module.params['group_tags']

        if not group_name:
            module.fail_json(msg='Group name is required to create security group')

        total_rules_count = 0
        inbound_rules = module.params['rules']
        if inbound_rules:
            total_rules_count = len(inbound_rules)
            validated, validation_msg = validate_sg_rules(inbound_rules)
            if not validated:
                module.fail_json(msg='Inbound rules failed validation. ' + validation_msg)

        outbound_rules = module.params['rules_egress']
        if outbound_rules:
            total_rules_count += len(outbound_rules)
            validated, validation_msg = validate_sg_rules(outbound_rules)
            if not validated:
                module.fail_json(msg='Outbound rules failed validation. ' + validation_msg)

        if total_rules_count > 100:
            module.fail_json(msg='more than 100 rules for authorization are not allowed')

        changed, security_group_id, result = create_security_group(module, ecs, group_name=group_name,
                                                                   group_description=group_description, vpc_id=vpc_id,
                                                                   group_tags=group_tags, inbound_rules=inbound_rules,
                                                                   outbound_rules=outbound_rules)

        module.exit_json(changed=changed, security_group_id=security_group_id, msg=result)

    elif state == 'getinfo':
        vpc_id = module.params['vpc_id']
        group_id = module.params['group_id']

        (changed, result) = get_security_status(module, ecs, vpc_id, group_id)
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


# import module snippets
from ansible.module_utils.basic import *

try:
    from ecsutils.ecs import *
    from footmark.exception import ECSResponseError

    HAS_ECS = True
except ImportError:
    HAS_ECS = False

# import ECSConnection
main()


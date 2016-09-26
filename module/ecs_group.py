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
    choices: [ "present", "absent" ]
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
    required: true
  vpc_id:
    description:
      - ID of the VPC to create the group in.
    required: false
  rules:
    description:
      - List of firewall inbound rules to enforce in this group. If none are supplied, a default all-out rule is assumed. If an empty list is supplied, no inbound rules will be enabled.
        Each rule contains four attributs as follows:
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

function delete a security group:
  group_id:
    description:
      - Name of the security group.
    required: true
    default: false
    aliases: [security_group_id]
'''

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
#!/usr/bin/python
# This file is part of Ansible

DOCUMENTATION = """
---
module: ecs_elb_lb
description:
  - Returns information about the load balancer.
  - Will be marked changed when called only if state is changed.
short_description: Creates or destroys Amazon SLB.
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
    description:
      - Create or destroy the SLB
    choices: ["present", "absent"]
    required: true

function create SLB
    description: create a SLB.
    state: present
    options:
      name:
        description:
          - The name of the SLB
        required: true
      address_type:
        description:
          - The address type of the SLB.
        default: internet
        required: false
        choices: ['internet', 'intranet']
      vswitch_id:
        description:
          - The vswitch id of the VPC instance.
        required: depends on
        default: null
      internet_charge_type:
        description:
          - The charge type of internet.
        required: false
        choices: ['paybybandwidth', 'paybytraffic']
        default: paybytraffic
      bandwidth:
        description:
          - The bandwidth of internet
        required: false
        default: null
      listeners:
        description:
          - List of ports/protocols for this SLB to listen on (see example)
        required: false
      purge_listeners:
        description:
          - Purge existing listeners on SLB that are not found in listeners
        required: false
        default: true
      instance_ids:
        description:
          - List of instance ids to attach to this SLB
        required: false
        default: false
      purge_instance_ids:
        description:
          - Purge existing instance ids on SLB that are not found in instance_ids
        required: false
        default: false
      zones:
        description:
          - List of availability zones to enable on this SLB
        required: false
      purge_zones:
        description:
          - Purge existing availability zones on SLB that are not found in zones
        required: false
        default: false
      health_check:
        description:
          - An associative array of health check configuration settings (see example)
        require: false
        default: None
      scheme:
        description:
          - The scheme to use when creating the SLB. For a private VPC-visible SLB use 'internal'.
        required: false
        default: 'internet-facing'
        version_added: "1.7"
      validate_certs:
        description:
          - When set to "no", SSL certificates will not be validated.
        required: false
        default: "yes"
        choices: ["yes", "no"]
        aliases: []
      stickiness:
        description:
          - An associative array of stickness policy settings. Policy will be applied to all listeners ( see example )
        required: false

function delete SLB
    description: delete a SLB.
    state: absent
    options:
      name:
        slb_id:
          - The ID of the SLB
        required: true
"""

EXAMPLES = """
# Note: None of these examples set acs_access_key, acs_secret_key, or region.
# It is assumed that their matching environment variables are set.
# Basic provisioning example (non-VPC)
- local_action:
    module: ecs_elb_lb
    name: "test-please-delete"
    state: present
    zones:
      - us-east-1a
      - us-east-1d
    listeners:
      - protocol: http # options are http, https, ssl, tcp
        load_balancer_port: 80
        instance_port: 80
        proxy_protocol: True
      - protocol: https
        load_balancer_port: 443
        instance_protocol: http # optional, defaults to value of protocol setting
        instance_port: 80
        # ssl certificate required for https or ssl
        ssl_certificate_id: "arn:acs:iam::123456789012:server-certificate/company/servercerts/ProdServerCert"
# Internal SLB example
- local_action:
    module: ecs_elb_lb
    name: "test-vpc"
    scheme: internal
    state: present
    instance_ids:
      - i-abcd1234
    purge_instance_ids: true
    listeners:
      - protocol: http # options are http, https, ssl, tcp
        load_balancer_port: 80
        instance_port: 80
# Configure a health check.
- local_action:
    module: ecs_elb_lb
    name: "test-please-delete"
    state: present
    zones:
      - us-east-1d
    listeners:
      - protocol: http
        load_balancer_port: 80
        instance_port: 80
    health_check:
        ping_protocol: http # options are http, https, ssl, tcp
        ping_port: 80
        ping_path: "/index.html" # not required for tcp or ssl
        response_timeout: 5 # seconds
        interval: 30 # seconds
        unhealthy_threshold: 2
        healthy_threshold: 10
# Ensure SLB is gone
- local_action:
    module: ecs_elb_lb
    name: "test-please-delete"
    state: absent
# Normally, this module will purge any listeners that exist on the SLB
# but aren't specified in the listeners parameter. If purge_listeners is
# false it leaves them alone
- local_action:
    module: ecs_elb_lb
    name: "test-please-delete"
    state: present
    zones:
      - us-east-1a
      - us-east-1d
    listeners:
      - protocol: http
        load_balancer_port: 80
        instance_port: 80
    purge_listeners: no
# Normally, this module will leave availability zones that are enabled
# on the SLB alone. If purge_zones is true, then any extraneous zones
# will be removed
- local_action:
    module: ecs_elb_lb
    name: "test-please-delete"
    state: present
    zones:
      - us-east-1a
      - us-east-1d
    listeners:
      - protocol: http
        load_balancer_port: 80
        instance_port: 80
    purge_zones: yes
# Create an SLB with load balanacer stickiness enabled
- local_action:
    module: ecs_elb_lb
    name: "New SLB"
    state: present
    region: us-east-1
    zones:
      - us-east-1a
      - us-east-1d
    listeners:
      - protocol: http
      - load_balancer_port: 80
      - instance_port: 80
    stickiness:
      type: insert
      enabled: yes
      expiration: 300
# Create an SLB with application stickiness enabled
- local_action:
    module: ecs_elb_lb
    name: "New SLB"
    state: present
    region: us-east-1
    zones:
      - us-east-1a
      - us-east-1d
    listeners:
      - protocol: http
      - load_balancer_port: 80
      - instance_port: 80
    stickiness:
      type: server
      enabled: yes
      cookie: SESSIONID
"""
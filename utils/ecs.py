# This code is part of Ansible, but is an independent component.
# This file identifies and gains playbook params, and provides this params to ansible module ecs. 
# This file implements connection between ansible and Alicloud ecs api via footmark.
#
# Copyright (c), xiao zhu <heguimin36@163.com.com>, 2016.08
# All rights reserved.

import os
import sys
import footmark.ecs
import footmark.slb
import footmark.vpc


class AnsibleACSError(Exception):
    pass


def acs_common_argument_spec():
    return dict(
        acs_secret_access_key=dict(aliases=['ecs_secret_key', 'secret_key']),
        acs_access_key=dict(aliases=['ecs_access_key', 'access_key']),
        security_token=dict(aliases=['access_token'], no_log=True),
    )


def ecs_argument_spec():
    spec = acs_common_argument_spec()
    spec.update(
        dict(
            region=dict(aliases=['acs_region', 'ecs_region']),
        )
    )
    return spec


def get_acs_connection_info(module):
    """
    Check module args for credentials, then check environment vars access_key
    :param module: Ansible module
    :return:
    """

    access_key = module.params.get('acs_access_key')
    secret_key = module.params.get('acs_secret_access_key')
    security_token = module.params.get('security_token')
    region = module.params.get('region')

    if not access_key:
        if 'ACS_ACCESS_KEY_ID' in os.environ:
            access_key = os.environ['ACS_ACCESS_KEY_ID']
        elif 'ACS_ACCESS_KEY' in os.environ:
            access_key = os.environ['ACS_ACCESS_KEY']
        elif 'ECS_ACCESS_KEY' in os.environ:
            access_key = os.environ['ECS_ACCESS_KEY']
        else:
            # in case access_key came in as empty string
            module.fail_json(msg="access key is required")

    if not secret_key:
        if 'ACS_SECRET_ACCESS_KEY' in os.environ:
            secret_key = os.environ['ACS_SECRET_ACCESS_KEY']
        elif 'ACS_SECRET_KEY' in os.environ:
            secret_key = os.environ['ACS_SECRET_KEY']
        elif 'ECS_SECRET_KEY' in os.environ:
            secret_key = os.environ['ECS_SECRET_KEY']
        else:
            # in case secret_key came in as empty string
            module.fail_json(msg="access secret key is required")

    if not region:
        if 'ACS_REGION' in os.environ:
            region = os.environ['ACS_REGION']
        elif 'ACS_DEFAULT_REGION' in os.environ:
            region = os.environ['ACS_DEFAULT_REGION']
        elif 'ECS_REGION' in os.environ:
            region = os.environ['ECS_REGION']
        else:
            module.fail_json(msg="region is required")

    if not security_token:
        if 'ACS_SECURITY_TOKEN' in os.environ:
            security_token = os.environ['ACS_SECURITY_TOKEN']
        elif 'ECS_SECURITY_TOKEN' in os.environ:
            security_token = os.environ['ECS_SECURITY_TOKEN']
        else:
            # in case security_token came in as empty string
            security_token = None

    ecs_params = dict(acs_access_key_id=access_key, acs_secret_access_key=secret_key, security_token=security_token)

    return region, ecs_params


def connect_to_acs(acs_module, region, **params):
    conn = acs_module.connect_to_region(region, **params)     
    if not conn:
        if region not in [acs_module_region.id for acs_module_region in acs_module.regions()]:
            raise AnsibleACSError(
                "Region %s does not seem to be available for acs module %s." % (region, acs_module.__name__))
        else:
            raise AnsibleACSError(
                "Unknown problem connecting to region %s for acs module %s." % (region, acs_module.__name__))
    return conn


def ecs_connect(module):
    """ Return an ecs connection"""

    region, ecs_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            ecs = connect_to_acs(footmark.ecs, region, **ecs_params)
        except AnsibleACSError, e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return ecs


def slb_connect(module):
    """ Return an slb connection"""

    region, slb_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            slb = connect_to_acs(footmark.slb, region, **slb_params)
        except AnsibleACSError, e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return slb


def vpc_connect(module):
    """ Return an vpc connection"""

    region, vpc_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            vpc = connect_to_acs(footmark.vpc, region, **vpc_params)
        except AnsibleACSError, e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return vpc
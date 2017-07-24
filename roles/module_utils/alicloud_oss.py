# This code is part of Ansible, but is an independent component.
# This file identifies and gains playbook params, and provides this params to ansible module ecs. 
# This file implements connection between ansible and Alicloud ecs api via footmark.
#
# Copyright (c), xiao zhu <heguimin36@163.com.com>, 2016.08
# All rights reserved.

import os
from ansible.release import __version__
import footmark.oss
#
# try:
#     import footmark.oss
# except ImportError:
#     raise ImportError('footmark is required for the module')


class AnsibleACSError(Exception):
    pass


def acs_common_argument_spec():
    return dict(
        alicloud_access_key=dict(aliases=['acs_access_key', 'ecs_access_key', 'access_key']),
        alicloud_secret_key=dict(aliases=['acs_secret_access_key', 'ecs_secret_key', 'secret_key']),
    )


def oss_bucket_argument_spec():
    spec = acs_common_argument_spec()
    spec.update(
        dict(
            alicloud_region=dict(aliases=['acs_region', 'ecs_region', 'region']),
            bucket=dict(aliases=['bucket_name', 'name'], type='str', required='True')
        )
    )
    return spec


def get_oss_connection_info(module):
    '''
    Check module args for credentials, then check environment vars access_key
    '''
    access_key = module.params.get('alicloud_access_key')
    secret_key = module.params.get('alicloud_secret_key')
    region = module.params.get('alicloud_region')

    if not access_key:
        if 'ALICLOUD_ACCESS_KEY' in os.environ:
            access_key = os.environ['ALICLOUD_ACCESS_KEY']
        elif 'ACS_ACCESS_KEY_ID' in os.environ:
            access_key = os.environ['ACS_ACCESS_KEY_ID']
        elif 'ACS_ACCESS_KEY' in os.environ:
            access_key = os.environ['ACS_ACCESS_KEY']
        elif 'ECS_ACCESS_KEY' in os.environ:
            access_key = os.environ['ECS_ACCESS_KEY']
        else:
            # in case access_key came in as empty string
            module.fail_json(msg="access key is required")

    if not secret_key:
        if 'ALICLOUD_SECRET_KEY' in os.environ:
            secret_key = os.environ['ALICLOUD_SECRET_KEY']
        elif 'ACS_SECRET_ACCESS_KEY' in os.environ:
            secret_key = os.environ['ACS_SECRET_ACCESS_KEY']
        elif 'ACS_SECRET_KEY' in os.environ:
            secret_key = os.environ['ACS_SECRET_KEY']
        elif 'ECS_SECRET_KEY' in os.environ:
            secret_key = os.environ['ECS_SECRET_KEY']
        else:
            # in case secret_key came in as empty string
            module.fail_json(msg="access secret key is required")

    if not region:
        if 'ALICLOUD_REGION' in os.environ:
            region = os.environ['ALICLOUD_REGION']
        elif 'ACS_REGION' in os.environ:
            region = os.environ['ACS_REGION']
        elif 'ACS_DEFAULT_REGION' in os.environ:
            region = os.environ['ACS_DEFAULT_REGION']
        elif 'ECS_REGION' in os.environ:
            region = os.environ['ECS_REGION']
        else:
            module.fail_json(msg="region is required")

    oss_params = dict(acs_access_key_id=access_key, acs_secret_access_key=secret_key, user_agent='Ansible-v' + __version__)

    return region, oss_params


def get_bucket_connection_info(module):
    '''
    Check module args for credentials, then check environment vars access_key
    '''
    region, oss_params = get_oss_connection_info(module)
    bucket_name = module.params.get('bucket')

    if bucket_name is None:
        module.fail_json(msg="bucket name is required")

    oss_params.update(dict(bucket_name=bucket_name))

    return region, oss_params


def connect_to_oss(acs_module, region, **params):
    conn = acs_module.connect_to_oss(region, **params)
    return conn


def connect_to_oss_bucket(acs_module, region, **params):
    conn = acs_module.connect_to_bucket(region, **params)
    return conn


def oss_bucket_connect(module):
    """ Return an oss bucket connection"""

    region, oss_params = get_bucket_connection_info(module)
    try:
        return connect_to_oss_bucket(footmark.oss, region, **oss_params)
    except AnsibleACSError, e:
        module.fail_json(msg=str(e))


def oss_service_connect(module):
    """ Return an oss service connection"""

    region, oss_params = get_oss_connection_info(module)
    try:
        return connect_to_oss(footmark.oss, region, **oss_params)
    except AnsibleACSError, e:
        module.fail_json(msg=str(e))
# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os

try:
    import footmark
    import footmark.oss
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


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
    """ Check module args for credentials, then check environment vars access_key """

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

    oss_params = dict(acs_access_key_id=access_key, acs_secret_access_key=secret_key, user_agent='Ansible-Provider-Alicloud')

    return region, oss_params


def get_bucket_connection_info(module):
    """ Check module args for credentials, then check environment vars access_key """

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
    except AnsibleACSError as e:
        module.fail_json(msg=str(e))


def oss_service_connect(module):
    """ Return an oss service connection"""

    region, oss_params = get_oss_connection_info(module)
    try:
        return connect_to_oss(footmark.oss, region, **oss_params)
    except AnsibleACSError as e:
        module.fail_json(msg=str(e))

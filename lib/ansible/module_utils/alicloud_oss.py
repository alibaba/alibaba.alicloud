# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.alicloud_ecs import get_profile

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
        alicloud_access_key=dict(aliases=['access_key_id', 'access_key'], no_log=True,
                                 fallback=(env_fallback, ['ALICLOUD_ACCESS_KEY', 'ALICLOUD_ACCESS_KEY_ID'])),
        alicloud_secret_key=dict(aliases=['secret_access_key', 'secret_key'], no_log=True,
                                 fallback=(env_fallback, ['ALICLOUD_SECRET_KEY', 'ALICLOUD_SECRET_ACCESS_KEY'])),
        alicloud_security_token=dict(aliases=['security_token'], no_log=True,
                                     fallback=(env_fallback, ['ALICLOUD_SECURITY_TOKEN'])),
        ecs_role_name=dict(aliases=['role_name'], fallback=(env_fallback, ['ALICLOUD_ECS_ROLE_NAME']))
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


def update_credential(module):
    acs_params = get_profile(module.params)
    acs_params.pop("ecs_role_name")

    return acs_params


def get_bucket_connection_info(module):
    """ Check module args for credentials, then check environment vars access_key """

    acs_params = update_credential(module)
    # If we have a region specified, connect to its endpoint.
    region = module.params.get('alicloud_region')
    bucket_name = module.params.get('bucket')

    if bucket_name is None:
        module.fail_json(msg="bucket name is required")

    acs_params.update(dict(bucket_name=bucket_name))

    return region, acs_params


def oss_connect(module):
    """ Return a oss connection"""
    acs_params = update_credential(module)
    # If we have a region specified, connect to its endpoint.
    region = module.params.get('alicloud_region')
    if region:
        try:
            conn = module.connect_to_oss(region, **acs_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
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
    try:
        return oss_connect(footmark.oss)
    except AnsibleACSError as e:
        module.fail_json(msg=str(e))

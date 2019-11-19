# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com>
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

try:
    import footmark
    import footmark.ecs
    import footmark.slb
    import footmark.vpc
    import footmark.rds
    import footmark.ess
    import footmark.sts
    import footmark.dns
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


def ecs_argument_spec():
    spec = acs_common_argument_spec()
    spec.update(
        dict(
            alicloud_region=dict(required=True, aliases=['region', 'region_id'],
                                 fallback=(env_fallback, ['ALICLOUD_REGION', 'ALICLOUD_REGION_ID'])),
            alicloud_assume_role_arn=dict(aliases=['assume_role_arn'], fallback=(env_fallback, ['ALICLOUD_ASSUME_ROLE_ARN'])),
            alicloud_assume_role_session_name=dict(aliases=['assume_role_session_name'],
                                       fallback=(env_fallback, ['ALICLOUD_ASSUME_ROLE_SESSION_NAME'])),
            alicloud_assume_role_session_expiration=dict(aliases=['assume_role_session_expiration'],
                                             fallback=(env_fallback, ['ALICLOUD_ASSUME_ROLE_SESSION_EXPIRATION'])),
            alicloud_assume_role_policy=dict(aliases=['assume_role_policy']),
        )
    )
    return spec


def get_acs_connection_info(module):

    ecs_params = dict(acs_access_key_id=module.params.get('alicloud_access_key'),
                      acs_secret_access_key=module.params.get('alicloud_secret_key'),
                      security_token=module.params.get('alicloud_security_token'),
                      ecs_role_name=module.params.get('ecs_role_name'),
                      user_agent='Ansible-Provider-Alicloud')

    return module.params.get('alicloud_region'), ecs_params


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


def get_assume_role(module):
    """ Return new params """
    region, sts_params = get_acs_connection_info(module)
    assume_role_params = {
        'role_arn': module.params.get('alicloud_assume_role_arn'),
        'role_session_name': module.params.get('alicloud_assume_role_session_name'),
        'duration_seconds': module.params.get('alicloud_assume_role_session_expiration'),
        'policy': module.params.get('alicloud_assume_role_policy')
    }

    try:
        sts = connect_to_acs(footmark.sts, region, **sts_params).assume_role(**assume_role_params).read()
        sts_params['acs_access_key_id'], sts_params['acs_secret_access_key'], sts_params['security_token'] \
            = sts['access_key_id'], sts['access_key_secret'], sts['security_token']
    except AnsibleACSError as e:
        module.fail_json(msg=str(e))
    return sts_params


def ecs_connect(module):
    """ Return an ecs connection"""

    region, ecs_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            if module.params['alicloud_assume_role_arn']:
                ecs_params = get_assume_role(module)
            ecs = connect_to_acs(footmark.ecs, region, **ecs_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return ecs


def slb_connect(module):
    """ Return an slb connection"""

    region, slb_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            if module.params['alicloud_assume_role_arn']:
                slb_params = get_assume_role(module)
            slb = connect_to_acs(footmark.slb, region, **slb_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return slb


def dns_connect(module):
    """ Return an dns connection"""

    region, dns_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            if module.params['alicloud_assume_role_arn']:
                dns_params = get_assume_role(module)
            dns = connect_to_acs(footmark.dns, region, **dns_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return dns


def vpc_connect(module):
    """ Return an vpc connection"""

    region, vpc_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            if module.params['alicloud_assume_role_arn']:
                vpc_params = get_assume_role(module)
            vpc = connect_to_acs(footmark.vpc, region, **vpc_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return vpc


def rds_connect(module):
    """ Return an rds connection"""

    region, rds_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            if module.params['alicloud_assume_role_arn']:
                rds_params = get_assume_role(module)
            rds = connect_to_acs(footmark.rds, region, **rds_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return rds


def ess_connect(module):
    """ Return an ess connection"""

    region, ess_params = get_acs_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            if module.params['alicloud_assume_role_arn']:
                ess_params = get_assume_role(module)
            ess = connect_to_acs(footmark.ess, region, **ess_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return ess
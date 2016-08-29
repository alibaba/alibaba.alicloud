# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c), Michael DeHaan <michael.dehaan@gmail.com>, 2012-2013
# All rights reserved.
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

import os
from time import sleep

import koball.ecs.module as ecs_module

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

    # Check module args for credentials, then check environment vars
    # access_key

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
            access_key = None

    if not secret_key:
        if 'ACS_SECRET_ACCESS_KEY' in os.environ:
            secret_key = os.environ['ACS_SECRET_ACCESS_KEY']
        elif 'ACS_SECRET_KEY' in os.environ:
            secret_key = os.environ['ACS_SECRET_KEY']
        elif 'ECS_SECRET_KEY' in os.environ:
            secret_key = os.environ['ECS_SECRET_KEY']
        else:
            # in case secret_key came in as empty string
            secret_key = None

    if not region:
        if 'ACS_REGION' in os.environ:
            region = os.environ['ACS_REGION']
        elif 'ACS_DEFAULT_REGION' in os.environ:
            region = os.environ['ACS_DEFAULT_REGION']
        elif 'ECS_REGION' in os.environ:
            region = os.environ['ECS_REGION']
        else:
            region = None

    if not security_token:
        if 'ACS_SECURITY_TOKEN' in os.environ:
            security_token = os.environ['ACS_SECURITY_TOKEN']
        elif 'ECS_SECURITY_TOKEN' in os.environ:
            security_token = os.environ['ECS_SECURITY_TOKEN']
        else:
            # in case security_token came in as empty string
            security_token = None

    ecs_params = dict(acs_access_key=access_key, acs_secret_access_key=secret_key, security_token=security_token)
    
    # for param, value in ecs_params.items():
    #     if isinstance(value, str):
    #         ecs_params[param] = unicode(value, 'utf-8', 'strict')

    return region, ecs_params

def connect_to_acs(acs_module, region, **params):
    conn = acs_module.connect_to_region(region, **params)
    if not conn:
        if region not in [acs_module_region.id for acs_module_region in acs_module.regions()]:
            raise AnsibleACSError("Region %s does not seem to be available for acs module %s." % (region, acs_module.__name__))
        else:
            raise AnsibleACSError("Unknown problem connecting to region %s for acs module %s." % (region, acs_module.__name__))
    return conn


def ecs_connect(module):
    """ Return an ecs connection"""

    region, ecs_params = get_acs_connection_info(module)
    # # If we have a region specified, connect to its endpoint.
    if region:
        try:
            ecs = connect_to_acs(ecs_module, region, **ecs_params)
        except AnsibleACSError, e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return ecs

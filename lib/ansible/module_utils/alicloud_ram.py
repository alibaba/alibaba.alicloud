# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2017 Alibaba Group Holding Limited. Zhu Wei <rockzhu3344@sina.com>
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
    import footmark.ram
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


class AnsibleACSError(Exception):
    pass


def acs_common_argument_spec():
    return dict(
        alicloud_access_key=dict(required=True, aliases=['access_key_id', 'access_key'], no_log=True,
                                 fallback=(env_fallback, ['ALICLOUD_ACCESS_KEY', 'ALICLOUD_ACCESS_KEY_ID'])),
        alicloud_secret_key=dict(required=True, aliases=['secret_access_key', 'secret_key'], no_log=True,
                                 fallback=(env_fallback, ['ALICLOUD_SECRET_KEY', 'ALICLOUD_SECRET_ACCESS_KEY'])),
        alicloud_security_token=dict(aliases=['security_token'], no_log=True,
                                     fallback=(env_fallback, ['ALICLOUD_SECURITY_TOKEN'])),
    )

def ram_argument_spec():
    spec = acs_common_argument_spec()
    spec.update(
        dict(
            alicloud_region=dict(required=True, aliases=['region', 'region_id'],
                                 fallback=(env_fallback, ['ALICLOUD_REGION', 'ALICLOUD_REGION_ID'])),
        )
    )
    return spec

def get_ram_connection_info(module):
    ram_params = dict(acs_access_key_id=module.params.get('alicloud_access_key'),
                      acs_secret_access_key=module.params.get('alicloud_secret_key'),
                      security_token=module.params.get('alicloud_security_token'),
                      user_agent='Ansible-Provider-Alicloud')

    return module.params.get('alicloud_region'), ram_params

def ram_connect(module):
    """ Return an ecs connection"""
    region, ram_params = get_ram_connection_info(module)
    # If we have a region specified, connect to its endpoint.
    if region:
        try:
            ram = connect_to_acs(footmark.ram, region, **ram_params)
        except AnsibleACSError as e:
            module.fail_json(msg=str(e))
    # Otherwise, no region so we fallback to the old connection method
    return ram

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
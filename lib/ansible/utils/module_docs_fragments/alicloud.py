# !/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.


class ModuleDocFragment(object):

    # Alicloud only documentation fragment
    DOCUMENTATION = """
options:
  alicloud_access_key:
    description:
      - Alibaba Cloud access key. If not set then the value of environment variable C(ALICLOUD_ACCESS_KEY),
        C(ALICLOUD_ACCESS_KEY_ID) will be used instead.
    aliases: ['access_key_id', 'access_key']
  alicloud_secret_key:
    description:
      - Alibaba Cloud secret key. If not set then the value of environment variable C(ALICLOUD_SECRET_KEY),
        C(ALICLOUD_SECRET_ACCESS_KEY) will be used instead.
    aliases: ['secret_access_key', 'secret_key']
  alicloud_region:
    description:
      - The Alibaba Cloud region to use. If not specified then the value of environment variable
        C(ALICLOUD_REGION), C(ALICLOUD_REGION_ID) will be used instead.
    aliases: ['region', 'region_id']
  alicloud_security_token:
    description:
      - The Alibaba Cloud security token. If not specified then the value of environment variable
        C(ALICLOUD_SECURITY_TOKEN) will be used instead.
    aliases: ['security_token']
  alicloud_assume_role_arn:
    description:
      - The Alibaba Cloud role_arn. The ARN of the role to assume. If ARN is set to an empty string, 
        it does not perform role switching. It supports environment variable ALICLOUD_ASSUME_ROLE_ARN. 
        ansible will execute with provided credentials.
    aliases: ['assume_role_arn']
  alicloud_assume_role_session_name:
    description:
      - The Alibaba Cloud session_name. The session name to use when assuming the role. If omitted, 
        'ansible' is passed to the AssumeRole call as session name. It supports environment variable 
        ALICLOUD_ASSUME_ROLE_SESSION_NAME
    aliases: ['assume_role_session_name']
  alicloud_assume_role_session_expiration:
    description:
      - The Alibaba Cloud session_expiration. The time after which the established session for assuming 
        role expires. Valid value range: [900-3600] seconds. Default to 3600 (in this case Alicloud use own default 
        value). It supports environment variable ALICLOUD_ASSUME_ROLE_SESSION_EXPIRATION
    aliases: ['assume_role_session_expiration']
  alicloud_assume_role_policy:
    description:
      - The Alibaba Cloud policy. A more restrictive policy to apply to the temporary credentials. 
        This gives you a way to further restrict the permissions for the resulting temporary security credentials. 
        You cannot use the passed policy to grant permissions that are in excess of those allowed by the access policy
        of the role that is being assumed.
    aliases: ['assume_role_policy']   

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
extends_documentation_fragment:
    - alicloud
notes:
  - If parameters are not set within the module, the following
    environment variables can be used in decreasing order of precedence
    C(ALICLOUD_ACCESS_KEY) or C(ALICLOUD_ACCESS_KEY_ID),
    C(ALICLOUD_SECRET_KEY) or C(ALICLOUD_SECRET_ACCESS_KEY),
    C(ALICLOUD_REGION) or C(ALICLOUD_REGION_ID),
    C(ALICLOUD_SECURITY_TOKEN)
  - C(ALICLOUD_REGION) or C(ALICLOUD_REGION_ID) can be typically be used to specify the
    ALICLOUD region, when required, but this can also be configured in the footmark config file
"""

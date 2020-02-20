#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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
# along with Ansible. If not, see http://www.gnu.org/licenses/.


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: ali_slb_tag
version_added: "2.9"
short_description: Add tags for Alibaba Cloud SLB resource.
description:
    - Add tags to Alibaba Cloud SLB resources
options:
  state:
    description:
      -  Whether or not to add, remove tags.
    choices: ['present', 'absent']
    default: 'present'
  resource_ids:
    description:
      - A list of slb ids.
  resource_type:
    description:
      - The type of SLB resource.
    default: 'instance'
  tags:
    description:
      - A hash/dictionaries of resource tags. C({"key":"value"})
requirements:
    - "python >= 3.6"
    - "footmark >= 1.17.0"
extends_documentation_fragment:
    - alicloud
author:
  - "He Guimin (@xiaozhu36)"
"""

EXAMPLES = """
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.
- name: Changed. Add Tags.
  ali_slb_tag:
    resource_type: 'instance'
    resource_ids: [lb_id, lb_id1]
    tags: {
            "Ansible": "Add tags"
    }

- name: Changed. Remove Tags.
  ali_slb_tag:
    state: absent
    resource_type: 'instance'
    resource_ids: [lb_id, lb_id1]
    tags: {
      "Ansible": "Add tags"
    }
"""

RETURN = '''
tags:
    description:
      - info about the server load balancer that was added tags.
    returned: always
    type: complex
    contains:
        tags:
            description: Tags of resource.
            returned: always
            type: complex
            sample: {"tag_key": "tag_value"}
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, slb_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import SLBResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def slb_exists(module, conn):
    try:
        return conn.describe_load_balancers(load_balancer_id=','.join(module.params['resource_ids']))
    except Exception as e:
        module.fail_json(msg="Failed to describe slbs: {0}".format(e))
    return None


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        resource_ids=dict(type='list'),
        resource_type=dict(type='str', default='instance'),
        tags=dict(type='dict')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_slb_tag.')

    slb_conn = slb_connect(module)
    slbs = slb_exists(module, slb_conn)

    if not slbs:
        module.fail_json(msg='No matching SLB was found based on the IDS provided.')

    # Get values of variable
    tags = module.params['tags']

    if module.params['state'] == "present":
        slb_changed = slb_conn.tag_resources(resource_ids=module.params['resource_ids'], tags=tags, resource_type=module.params['resource_type'])
    else:
        slb_changed = slb_conn.untag_resources(resource_ids=module.params['resource_ids'], tags=tags, resource_type=module.params['resource_type'])

    result = []
    for slb in slbs:
        result.append(slb.get().read())

    module.exit_json(changed=slb_changed, tags=result)


if __name__ == '__main__':
    main()

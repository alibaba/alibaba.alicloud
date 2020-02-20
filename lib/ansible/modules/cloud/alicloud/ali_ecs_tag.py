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
module: ali_ecs_tag
version_added: "2.9"
short_description: Add tags for Alibaba Cloud resource.
description:
    - Add tags to Alibaba Cloud resources
options:
  state:
    description:
      -  Whether or not to add, remove tags.
    choices: ['present', 'absent']
    default: 'present'
  resource_ids:
    description:
      - A list of resource ids.
  resource_type:
    description:
      - The type of resource.
    choices: ['instance', 'disk', 'image', 'eni', 'securitygroup']
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
  ali_ecs_tag:
    resource_type: 'instance'
    resource_ids: [i_id, i_id1]
    tags: {
            "Ansible": "Add tags"
    }

- name: Changed. Remove Tags.
  ali_ecs_tag:
    state: absent
    resource_type: 'instance'
    resource_ids: [i_id, i_id1]
    tags: {
      "Ansible": "Add tags"
    }
"""

RETURN = '''
tags:
    description:
      - info about the resource that was added tags.
    returned: always
    type: complex
    contains:
        tags:
            description: The resource tags.
            returned: always
            type: complex
            sample: {"tag_key": "tag_value"}
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def ecs_exists(module, conn):
    try:
        return conn.describe_instances(instance_ids=module.params["resource_ids"])
    except Exception as e:
        module.fail_json(msg="Failed to describe ecs instances: {0}".format(e))
    return None


def disk_exists(module, conn):
    try:
        disk_l = []
        result = conn.describe_disks()
        for res in result:
            if res.id in module.params['resource_ids']:
                disk_l.append(res)
        return disk_l
    except Exception as e:
        module.fail_json(msg="Failed to describe disks: {0}".format(e))
    return None


def image_exists(module, conn):
    try:
        image_l = []
        result = conn.describe_images()
        for res in result:
            if res.id in module.params['resource_ids']:
                image_l.append(res)
        return image_l
    except Exception as e:
        module.fail_json(msg="Failed to describe images: {0}".format(e))
    return None


def sgroup_exists(module, conn):
    try:
        sgroup_l = []
        result = conn.describe_security_groups()
        for res in result:
            if res.id in module.params['resource_ids']:
                sgroup_l.append(res)
        return sgroup_l
    except Exception as e:
        module.fail_json(msg="Failed to describe security group: {0}".format(e))
    return None


def eni_exists(module, conn):
    try:
        eni_l = []
        result = conn.describe_network_interfaces()
        for res in result:
            if res.id in module.params['resource_ids']:
                eni_l.append(res)
        return eni_l
    except Exception as e:
        module.fail_json(msg="Failed to describe network interfaces: {0}".format(e))
    return None


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        state=dict(default='present', choices=['present', 'absent']),
        resource_ids=dict(type='list', required=True),
        resource_type=dict(type='str', default='instance', choices=['instance', 'disk', 'image', 'eni', 'securitygroup']),
        tags=dict(type='dict')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module ali_ecs_tag.')

    ecs_conn = ecs_connect(module)
    if module.params['resource_type'] == 'instance':
        resources = ecs_exists(module, ecs_conn)
    elif module.params['resource_type'] == 'disk':
        resources = disk_exists(module, ecs_conn)
    elif module.params['resource_type'] == 'image':
        resources = image_exists(module, ecs_conn)
    elif module.params['resource_type'] == 'eni':
        resources = eni_exists(module, ecs_conn)
    else:
        resources = sgroup_exists(module, ecs_conn)

    if not resources:
        module.fail_json(msg='No matching resource was found based on the IDS provided.')

    #Get values of variable
    tags = module.params['tags']

    if module.params['state'] == "present":
        ecs_changed = ecs_conn.tag_resources(resource_ids=module.params['resource_ids'], tags=tags, resource_type=module.params['resource_type'])
    else:
        ecs_changed = ecs_conn.untag_resources(resource_ids=module.params['resource_ids'], tags=tags, resource_type=module.params['resource_type'])

    result = []
    for resource in resources:
        result.append(resource.read()['tags'])

    module.exit_json(changed=ecs_changed, tags=result)


if __name__ == '__main__':
    main()

#!/usr/bin/python
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
#  This file is part of Ansible
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_instance_type_facts
version_added: "2.4"
short_description: Gather facts of instance types provided by Alibaba Cloud ECS.
description:
     - This module fetches data from the Open API in Alicloud.

options:
    alicloud_zone:
      description:
        - The Zone that supports available instance types.
      aliases: ['zone_id', 'zone']
    instance_type_ids:
      description:
        - List Ids of instance types.
      aliases: ['ids']
    instance_type_families:
      description:
        - List family names of instance types.
      aliases: ['families']
    cpu_core_count:
      description:
        - Cpu core count of instance type.
      aliases: ['cpu_count']
    memory_size:
      description:
        - Memory size of instance type.
      aliases: ['memory']
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.1.16"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Fetch instance types according to setting different filters
- name: fetch instance types example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key>
    alicloud_secret_key: <your-alicloud-secret-key>
    alicloud_region: cn-beijing
    alicloud_zone: cn-beijing-a

  tasks:
    - name: Find all instance types in the specified region
      alicloud_instance_type_facts:
        alicloud_region: '{{ alicloud_region }}'
      register: all_instance_types
    - name: Find all instance types based on the specified zone
      alicloud_instance_type_facts:
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
      register: instance_types_by_zone
    - name: Find all instance types based on the specified family names
      alicloud_instance_type_facts:
        alicloud_region: '{{ alicloud_region }}'
        instance_type_families:
          - "ecs.gn5"
          - "ecs.sn2ne"
      register: instance_types_by_families
    - name: Find all instance types based on the specified ids
      alicloud_instance_type_facts:
        alicloud_region: '{{ alicloud_region }}'
        instance_type_ids:
         - "ecs.se1ne.14xlarge"
         - "ecs.m2.xlarge"
      register: instance_types_by_ids
    - name: Find all instance types based on the specified cpu core count
      alicloud_instance_type_facts:
        alicloud_region: '{{ alicloud_region }}'
        cpu_core_count: 56
      register: instance_types_by_cpu
    - name: Find all instance types based on the specified memory size
      alicloud_instance_type_facts:
        alicloud_region: '{{ alicloud_region }}'
        memory_size: 64.0
      register: instance_types_by_memory
'''

RETURN = '''
instance_type_ids:
    description: List ids of the instance types.
    returned: when success
    type: list
    sample: ["ecs.m1.medium", "ecs.m1.xlarge"]
instance_types:
    description: Details about the ecs instance types.
    returned: when success
    type: list
    sample: [{
        "cpu_core_count": 4,
        "id": "ecs.m1.medium",
        "instance_type_family": "ecs.m1",
        "memory_size": 16.0
    },
    {
        "cpu_core_count": 8,
        "id": "ecs.m1.xlarge",
        "instance_type_family": "ecs.m1",
        "memory_size": 32.0
    }]
total:
    description: The number of all instance types.
    returned: when success
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError

    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_instance_type_info(inst_type):
    """
    Retrieves instance type information
    returns it as a dictionary
    """
    return {
        'id': inst_type.id,
        'cpu_core_count': inst_type.cpu_core_count,
        'memory_size': inst_type.memory_size,
        'instance_type_family': inst_type.family,
    }


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(
        dict(
            alicloud_zone=dict(aliases=['zone_id', 'zone']),
            instance_type_ids=dict(type='list', aliases=["ids"]),
            instance_type_families=dict(type='list', aliases=["families"]),
            cpu_core_count=dict(type='int', aliases=["cpu_count"]),
            memory_size=dict(type='float', aliases=["memory"]),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for the module alicloud_instance_type_facts')

    ecs = ecs_connect(module)

    instance_types = []
    ids = []

    zone_id = module.params["alicloud_zone"]
    instance_type_ids = module.params["instance_type_ids"]
    instance_type_families = module.params["instance_type_families"]
    cpu_core_count = module.params["cpu_core_count"]
    memory_size = module.params["memory_size"]

    if zone_id:
        zones = ecs.describe_zones(zone_id=zone_id)
        families = [f for z in zones for resource in z.available_resources["resources_info"] for f in resource["instance_type_families"]["supported_instance_type_family"]]

        if instance_type_families:
            filter_families = [f for f in instance_type_families if f in families]
            if not filter_families:
                module.fail_json(msg="Instance type families {0} is not supported in the zone {1}. Expected instance type families: {2}.".format(instance_type_families, zone_id, families))
            families = filter_families

        families = list(set(families))
    else:
        families = [f.id for f in ecs.describe_instance_type_families() if not instance_type_families or f.id in instance_type_families]

    for family in families:
        for instance_type in ecs.describe_instance_types(instance_type_family=family):
            if cpu_core_count and instance_type.cpu_core_count != cpu_core_count:
                continue
            if memory_size and instance_type.memory_size != memory_size:
                continue
            if instance_type_ids and instance_type.id not in instance_type_ids:
                continue
            instance_types.append(get_instance_type_info(instance_type))
            ids.append(instance_type.id)

    module.exit_json(changed=False, instance_type_ids=ids, instance_types=instance_types,
                     total=len(instance_types))


if __name__ == '__main__':
    main()

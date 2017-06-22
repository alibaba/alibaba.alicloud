#!/usr/bin/python
#
# Copyright 2017 Alibaba Group Holding Limited.
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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = """
---
module: ecs_vpc_route_table
version_added: "2.4"
short_description: Create, Query or Delete route table.
description:
    - Create, Query or Delete vswitch which in the vpc.
options:
  status:
    description:
      -  Whether or not to create, delete or query vswitch.
    choices: ['present', 'absent', 'fetch']
    required: false
    default: present
    aliases: [ 'state' ]
  alicloud_zone:
    description: Aliyun availability zone ID which to launch the vswitch
    required: true
    default: null
    aliases: [ 'acs_zone', 'ecs_zone', 'zone_id', 'zone' ]
  vpc_id:
    description:
      - The ID of a VPC to which that Vswitch belongs.
    required: true
    default: null
  cidr_block:
    description:
      - The CIDR block representing the Vswitch e.g. 10.0.0.0/8. The value must be sub cidr_block of Vpc.
    required: true
    default: null
  vswitch_name:
    description:
      - The name of vswitch, which is a string of 2 to 128 Chinese or English characters. It must begin with an
        uppercase/lowercase letter or a Chinese character and can contain numerals, "_", or "-".
        It cannot begin with http:// or https://.
    required: false
    default: null
    aliases: [ 'name' ]
  description:
    description:
      - The description of vswitch, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
    required: false
    default: null
  vswitch_ids:
    description:
      - One VSwitch ID or list of VSwitch's IDs. It required when managing the existing VSwitch(es).
        Such as deleting VSwitch(es) and querying VSwitch(es) attribute.
    required: false
    default: null
    aliases: [ 'subnet_ids' ]
  is_default:
    description:
      - When retrieving VSwitch, it can mark the VSwitch is created by system.
    required: false
    default: null
    type: bool
  pagenumber:
    description:
      - Page number of the vswitch list. The start value is 1.
    required: false
    default: 1
  pagesize:
    description:
      - The number of lines per page set for paging query. The maximum value is 50.
    required: false
    default: 10
author:
  - "He Guimin (@xiaozhu36)"

"""

EXAMPLES = """

# basic provisioning example to create vswitch
- name: create vswitch
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    vpc_id: xxxxxxxxxx
    alicloud_zone: cn-hongkong-b
    cidr_block: '172.16.0.0/24'
    name: 'Demo_VSwitch'
    description: 'akashhttp://'
    state: present
  tasks:
    - name: create vswitch
      ecs_vpc_vswitch:
        alicloud_region: '{{ alicloud_region }}'
        cidr_block: '{{ cidr_blok }}'
        name: ''{{ name }}''
        description: '{{ description }}'
        vpc_id: '{{ vpc_id }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

# basic provisioning example to delete vswitch
- name: delete vswitch
  hosts: localhost
  connection: local
  vars:
    alicloud_region: cn-hongkong
    vpc_id: xxxxxxxxxx
    purge_vswitches:
     - xxxxxxxxxx
    state: present
  tasks:
    - name: delete vswitch
      ecs_vpc:
        alicloud_region: '{{ alicloud_region }}'
        vpc_id: '{{ vpc_id }}'
        purge_vswitches: '{{ purge_vswitches }}'
        state: '{{ state }}'
      register: result
    - debug: var=result

"""

# import module snippets
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, vpc_connect
from footmark.exception import VPCResponseError

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_vswitch_dict(vswitch):
    """
    Format vpc result and returns it as a dictionary
    """

    return ({'id': vswitch.id, 'cidr_block': vswitch.cidr_block, 'available_ip_count': vswitch.available_ip_address_count,
             "creation_time": vswitch.creation_time, 'vpc_id': vswitch.vpc_id, 'zone_id': vswitch.zone_id,
             'status': vswitch.status, 'name': vswitch.name, 'description': vswitch.description, 'is_default': vswitch.is_default})


def create_vswitch(module, vpc):
    """
    Create VSwitch
    :param module: Ansible module object
    :param vpc: Authenticated vpc connection object
    :return: Return details of created VSwitch
    """
    zone_id = module.params['alicloud_zone']
    vpc_id = module.params['vpc_id']
    cidr_block = module.params['cidr_block']
    vsw_name = module.params['vswitch_name']
    description = module.params['description']

    if not vpc_id:
        module.fail_json(msg='vpc_id is required for creating a vswitch')

    if not zone_id:
        module.fail_json(msg='alicloud_zone is required for creating a vswitch')

    if not cidr_block:
        module.fail_json(msg='cidr_block is required for creating a vswitch')

    if str(description).startswith('http://') or str(description).startswith('https://'):
        module.fail_json(msg='description can not start with http:// or https://')

    if str(vsw_name).startswith('http://') or str(vsw_name).startswith('https://'):
        module.fail_json(msg='vswitch_name can not start with http:// or https://')

    changed = False
    try:
        changed, vswitch = vpc.create_vswitch(zone_id=zone_id, vpc_id=vpc_id, cidr_block=cidr_block,
                                              vswitch_name=None, description=None)
        return changed, get_vswitch_dict(vswitch)
    except VPCResponseError as e:
        module.fail_json(msg='Unable to create Vswitch, error: {0}'.format(e))

    return changed, None


def check_vswitch_vpc(module, vpc, vpc_id, vswitch_ids):
    """
    Delete VSwitch
    :param module: Ansible module object
    :param vpc: Authenticated vpc connection object
    :param vpc_id: ID of Vpc
    :param vswitch_ids: The IDs of the VSwitches to be deleted
    :return: Return the list ID of deleted VSwitches.
    """
    vpc_obj = vpc.get_vpc_attribute(vpc_id)
    if not vpc_obj:
        module.fail_json(msg='The specified vpc is not found, vpc_id: {0}.'.format(vpc_id))

    for vsw_id in vswitch_ids:
        if vsw_id not in vpc_obj.vswitch_ids['vswitch_id']:
            module.fail_json(msg='The specified vswitch: {0} is not found in the vpc: {0}.'.format(vsw_id, vpc_id))
    return


def delete_vswitch(module, vpc):
    """
    Delete VSwitch
    :param module: Ansible module object
    :param vpc: Authenticated vpc connection object
    :param vpc_id: ID of Vpc
    :param vswitch_ids: The IDs of the VSwitches to be deleted
    :return: Return the list ID of deleted VSwitches.
    """
    vpc_id = module.params['vpc_id']
    vswitch_ids = module.params['vswitch_ids']

    if isinstance(vswitch_ids, str):
        if not vswitch_ids.startswith("vsw"):
            module.fail_json(msg='vswitch_ids: {0} is invalid ID of vswitch, aborting.'.format(vswitch_ids))
        vswitch_ids = [vswitch_ids]

    if vswitch_ids and not isinstance(vswitch_ids, list):
        module.fail_json(msg='vswitch_ids: {0} should be a list of ids, aborting.'.format(vswitch_ids))

    if vpc_id and vswitch_ids:
        check_vswitch_vpc(module, vpc, vpc_id, vswitch_ids)
        for vsw_id in vswitch_ids:
            if not vpc.delete_vswitch(vsw_id):
                module.fail_json(msg='Deleting the specified vswitch: {0} failed.'.format(vsw_id))
        return vswitch_ids
    elif vpc_id:
        return vpc.delete_vswitch_with_vpc(vpc_id)
    elif vswitch_ids:
        for vsw_id in vswitch_ids:
            if not vpc.delete_vswitch(vsw_id):
                module.fail_json(msg='Deleting the specified vswitch: {0} failed.'.format(vsw_id))
        return vswitch_ids
    else:
        module.fail_json(msg='When deleting vswitch, vpc_id or vswitch_ids must be specified.')

    return None


def retrieve_vswitches(module, vpc):
    """
    Retrieve VPC
    :param module: Ansible module object
    :param vpc: Authenticated vpc connection object
    :return: Returns a list of VPC
    """
    vpc_id = module.params['vpc_id']
    vswitch_ids = module.params['vswitch_ids']
    zone_id = module.params['alicloud_zone']
    is_default = module.params['is_default']
    pagenumber = module.params['pagenumber']
    pagesize = module.params['pagesize']

    if isinstance(vswitch_ids, str):
        if not vswitch_ids.startswith("vsw"):
            module.fail_json(msg='vswitch_ids: {0} is invalid ID of vswitch, aborting.'.format(vswitch_ids))
        vswitch_ids = [vswitch_ids]

    if vswitch_ids and not isinstance(vswitch_ids, list):
        module.fail_json(msg='vswitch_ids: {0} should be a list of ids, aborting.'.format(vswitch_ids))

    if vpc_id and vswitch_ids:
        check_vswitch_vpc(module, vpc, vpc_id, vswitch_ids)

    vswitches = []
    try:
        results = vpc.get_all_vswitches(vpc_id=vpc_id, zone_id=zone_id, is_default=is_default, pagenumber=pagenumber, pagesize=pagesize)

        for vsw in results:
            if not vswitch_ids:
                vswitches.append(get_vswitch_dict(vsw))
            elif str(vsw.id) in vswitch_ids:
                vswitches.append(get_vswitch_dict(vsw))

    except VPCResponseError as e:
        module.fail_json(msg='Unable to retrieve vswitch, error: {0}'.format(e))

    return vswitches


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        status=dict(default='present', aliases=['state'], choices=['present', 'absent', 'fetch']),
        cidr_block=dict(aliases=['cidr']),
        description=dict(),
        alicloud_zone=dict(aliases=['acs_zone', 'ecs_zone', 'zone_id', 'zone']),
        vpc_id=dict(),
        vswitch_name=dict(aliases=['name']),
        vswitch_ids=dict(aliases=['subnet_ids']),
        pagenumber=dict(type='int', default='1'),
        pagesize=dict(type='int', default='10'),
        is_default=dict(type='bool'),
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    vpc = vpc_connect(module)

    # Get values of variable
    status = module.params['status']

    if status == 'present':
        changed, vswitch = create_vswitch(module, vpc)
        module.exit_json(changed=changed, vswitch=vswitch, vswitch_id=vswitch['id'])

    elif status == 'absent':
        vswitch_ids = delete_vswitch(module, vpc)
        module.exit_json(changed=True, vswitch_ids=vswitch_ids, total_count=len(vswitch_ids))

    elif status == 'fetch':
        vswitches = retrieve_vswitches(module, vpc)
        vswitch_ids = []
        for vsw in vswitches:
            vswitch_ids.append(vsw['id'])
        module.exit_json(changed=False, vswitches=vswitches, vswitch_ids=vswitch_ids, total_count=len(vswitches))

    else:
        module.fail_json(msg='The expected state: {0}, {1} and {2}, but got {3}.'.format("present", "absent", "fetch", status))


if __name__ == '__main__':
    main()

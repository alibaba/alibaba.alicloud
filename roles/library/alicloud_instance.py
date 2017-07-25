#!/usr/bin/python
#
# Copyright (c) 2017 Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
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

DOCUMENTATION = '''
---
module: alicloud_instance
version_added: "2.4"
short_description: Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group.
description:
    - Create, start, stop, restart, retrieval, modify or terminate ecs instances.
    - Add or remove ecs instances to/from security group.
options:
    status:
      description:
        - The state of the instance after operating.
      required: false
      default: 'present'
      aliases: ['state']
      choices: [ 'present', 'running', 'stopped', 'restarted', 'absent', 'list', 'current' ]
    alicloud_zone:
      description: Aliyun availability zone ID in which to launch the instance
      required: false
      default: null
      aliases: ['acs_zone', 'ecs_zone', 'zone_id', 'zone' ]
    image_id:
      description: Image ID to use for the instance.
      required: true
      default: null
      aliases: [ 'image' ]
    instance_type:
      description: Instance type to use for the instance
      required: true
      default: null
      aliases: [ 'type' ]
    group_id:
      description: Security group id to use with the instance
      required: false
      default: null
    io_optimized:
      description: Whether instance is using optimized volumes.
      required: false
      default: False
      type: bool
    vswitch_id:
      description: The subnet ID in which to launch the instance (VPC).
      required: false
      default: null
      aliases: ['subnet_id']
    private_ip:
      description: Private IP address of the instance, which cannot be specified separately.
      required: false
      default: null
    instance_name:
      description:
        - The name of ECS instance, which is a string of 2 to 128 Chinese or English characters. It must begin with an
          uppercase/lowercase letter or a Chinese character and can contain numerals, ".", "_", or "-".
          It cannot begin with http:// or https://.
      required: false
      default: null
    description:
      description:
        - The description of ECS instance, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
      required: false
      default: null
    internet_data:
      description:
        - A hash/dictionaries of internet to the new instance
      required: false
      default: null
      suboptions:
          charge_type:
            description:
              - Internet charge type, which can be PayByTraffic or PayByBandwidth.
            required: false
            default: "PayByBandwidth"
            choices: ["PayByBandwidth", "PayByTraffic"]
          max_bandwidth_in:
            description:
              - Maximum incoming bandwidth from the public network, measured in Mbps (Mega bit per second).
            required: false
            default: 200
            choices: [1~200]
          max_bandwidth_out:
            description:
              - Maximum outgoing bandwidth to the public network, measured in Mbps (Mega bit per second).
            required: false
            default: 0
            choices: [0~100]
    host_name:
      description: Instance host name.
      required: false
      default: null
    password:
      description: The password to login instance.
      required: false
      default: null
    system_disk:
      description:
        - A hash/dictionaries of system disk to the new instance
      required: false
      default: null
      suboptions:
          disk_category:
            description:
              - Category of the system disk.
            required: false
            default: "cloud"
            choices: ["cloud", "cloud_efficiency", "cloud_ssd", "ephemeral_ssd"]
          disk_size:
            description:
              - Size of the system disk, in GB
            required: false
            default: max[40, ImageSize]
            choices: [40~500]
          disk_name:
            description:
              - Name of a system disk.
            required: false
            default: null
          disk_description:
            description:
              - Description of a system disk.
            required: false
            default: null
    count:
      description: The number of the new instance.
      required: false
      default: 1
    allocate_public_ip:
      description: Whether allocate a public ip for the new instance.
      required: false
      default: true
      aliases: [ 'assign_public_ip' ]
      type: bool
    bind_eip:
      description: ID of Elastic IP Address bind to the new instance.
      required: false
      default: null
    ids:
      description:
        - A list of identifier for this instance or set of instances, so that the module will be idempotent with respect to ECS instances.
          This identifier should not be reused for another call later on.
          For details, see the description of client token at U(https://help.aliyun.com/document_detail/25693.html?spm=5176.doc25499.2.7.mrVgE2).
        - The length of the ids is the same with count
      required: false
      default: null
      aliases: [ 'id' ]
    instance_charge_type:
      description:
        - The charge type of the instance.
      required: false
      choices: ["PrePaid", "PostPaid"]
      default: "PostPaid"
    period:
      description:
        - The charge duration of the instance, the value is vaild when instance_charge_type is "PrePaid".
      required: false
      choices: [1~9,12,24,36]
      default: null
    auto_renew:
      description:
        - Whether automate renew the charge of the instance.
      required: false
      type: bool
      default: false
    auto_renew_period:
      description:
        - The duration of the automatic renew the charge of the instance. It is vaild when auto_renew is true.
      required: false
      choices: [1, 2, 3, 6, 12]
      default: null
    instance_ids:
      description:
        - "A list of instance ids, currently used for states: running, stopped, restarted, absent,
          and applied to join or leave instances from security group."
      required: true
      default: null
      aliases: ["instance_id"]
    force:
      description:
        - "Whether force to operation, currently used fo states: stopped and restarted."
      required: false
      default: False
      type: bool
    instance_tags:
      description:
        - A list of hash/dictionaries of instance tags, '[{tag_key:"value", tag_value:"value"}]',
                    tag_key must be not null when tag_value isn't null
      required: false
      default: null
      aliases: ["tags"]
    attributes:
      description:
        - A list of hash/dictionaries of instance attributes. If it's set, the specified instance's attributes would be modified.
      required: false
      default: null
      suboptions:
          id:
            description:
              - ID of an ECS instance
            required: true
            default: null
          name:
            description:
              - Name of the instance to modify
            required: false
            default: null
          description:
            description:
              - Description of the instance to use
            required: false
            default: null
          password:
            description:
              - The password to login instance
            required: false
            default: null
          host_name:
            description:
              - Instance host name
            required: false
            default: null
    sg_action:
      description: The action of operating security group.
      required: true
      default: null
      choices: ['join', 'leave']
    page_number:
      description: Page number of the instance status list
      required: false
      default: 1
    page_size:
        description: Sets the number of lines per page for queries per page
        required: false
        default: 10
    wait:
      description:
        - wait for the AMI to be in state 'available' before returning.
      required: false
      default: "no"
      choices: [ "yes", "no" ]
    wait_timeout:
      description:
        - how long before wait gives up, in seconds
      required: false
      default: 300
author:
    - "He Guimin (@xiaozhu36)"
'''

EXAMPLES = '''
#
# provisioning new ecs instance
#

# basic provisioning example classic network
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    alicloud_zone: cn-beijing-a
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n1.small
    assign_public_ip: yes
  tasks:
    - name: classic network
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        image: '{{ image }}'
        instance_type: '{{ instance_type }}'
        count: 2
        assign_public_ip: '{{ assign_public_ip }}'

# basic provisioning example vpc network
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n1.small
    vswitch_id: xxxxxxxxxx
    assign_public_ip: no
  tasks:
    - name: vpc network
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        instance_type: '{{ instance_type }}'
        vswitch_id: '{{ vswitch_id }}'
        assign_public_ip: '{{ assign_public_ip }}'


# advanced example with tagging and host name password
- name: advanced provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n1.small
    group_id: xxxxxxxxxx
    host_name: myhost
    password: mypassword
  tasks:
    - name: tagging and host name password
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        instance_type: '{{ instance_type }}'
        assign_public_ip: yes
        group_id: '{{ group_id }}'
        instance_tags:
            - tag_key : postgress
              tag_value: 1
        host_name: '{{ host_name }}'
        password: '{{ password }}'
        wait: yes
        wait_timeout: 500

# single instance with internet data configuration and instance details
- name: advanced provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n1.small
    group_id: xxxxxxxxxx
    instance_name: myinstance
    description: my description
  tasks:
    - name: internet data configuration and instance details
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        instance_type: '{{ instance_type }}'
        group_id: '{{ group_id }}'
        instance_name: '{{ instance_name }}'
        description: '{{ description }}'
        internet_data:
            charge_type: PayByBandwidth
            max_bandwidth_in: 200
            max_bandwidth_out: 50

# example with system disk configuration and IO optimized
- name: advanced provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n1.small
    io_optimized: yes
    system_disk:
      disk_category: cloud_efficiency
      disk_size: 100
      disk_name: DiskName
      disk_description: Disk Description
  tasks:
    - name: additional volume
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        instance_type: '{{ instance_type }}'
        io_optimized: '{{ io_optimized }}'
        system_disk: '{{ system_disk }}'

# example with prepaid internet charge type configuration
- name: advanced provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n1.small
  tasks:
    - name: prepaid internet charge type configuration
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        instance_type: '{{ instance_type }}'
        assign_public_ip: yes
        instance_charge_type: PrePaid
        period: 1
        auto_renew: yes
        auto_renew_period: 3

#
# modifying attributes of ecs instance
#
- name: modify attribute example
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
  tasks:
    - name: modify attribute of multiple instances
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        attributes:
            - id:  xxxxxxxxxx
              name: InstanceName
              description: volume attributes
              password: mypassword
              host_name: hostName
            - id:  xxxxxxxxxx
              name: InstanceName
              description: volume attributes
              password: mypassword
              host_name: hostcomes

#
# querying instance status
#
- name: query instance status
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-beijing
    alicloud_zone: cn-beijing-a
    status: current
    pagenumber: 1
    pagesize: 10
  tasks:
    - name: query instance status from the particular zone
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        alicloud_zone: '{{ alicloud_zone }}'
        status: '{{ status }}'
        pagenumber: '{{ pagenumber }}'
        pagesize: '{{ pagesize }}'

#
# start or terminate instance
#
- name: start or terminate instance
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
    instance_ids: xxxxxxxxxx
    instance_tags:
    - tag_key: xz_test
      tag_value: '1.20'
    status: running
  tasks:
    - name: start instance
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        instance_tags: '{{ instance_tags }}'
        status: '{{ status }}'

#
# stop or restarted instance
#
- name: start stop restart instance
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
    instance_ids: xxxxxxxxxx
    instance_tags:
    - tag_key: xz_test
      tag_value: '1.20'
    force: False
    status: restarted
  tasks:
    - name: Restart instance
      ecs:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        instance_tags: '{{ instance_tags }}'
        status: '{{ status }}'

#
# add an instance to security group
#
- name: Add an instance to security group
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
    instance_id: xxxxxxxxxx
    group_id: xxxxxxxxxx
    sg_action: join
  tasks:
    - name: Add an instance to security group
      ecs:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_id: '{{ instance_id }}'
        group_id: '{{ group_id }}'
        sg_action: '{{ sg_action }}'

#
# remove instance from security group
#
- name: Remove an instance from security group
  hosts: localhost
  vars:
    alicloud_access_key: xxxxxxxxxx
    alicloud_secret_key: xxxxxxxxxx
    alicloud_region: cn-shenzhen
    instance_id: xxxxxxxxxx
    group_id: xxxxxxxxxx
    sg_action: leave
  tasks:
    - name: Remove an instance from security group
      ecs:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_id: '{{ instance_id }}'
        group_id: '{{ group_id }}'
        sg_action: '{{ sg_action }}'
'''

RETURN = '''
instance_ids:
    description: List all instances's id after operating ecs instance.
    returned: when success
    type: list
    sample: ["i-35b333d9","i-ddav***"]
instance_ips:
    description: List all instances's public ip address after operating ecs instance.
    returned: 'on create, modify and list'
    type: list
    sample: ["10.1.1.1","10.1.1.2"]
instance_statuses:
    description: List all instances's status after operating ecs instance except deleted.
    returned: when success
    type: list
    sample: ["running","stopped"]
instances:
    description: Details about the ecs instances that were created.
    returned: 'on create, modify and list'
    type: dict
    sample: {
        "block_device_mapping": {
            "d-2ze9mho1vp79mctdoro0": {
                "delete_on_termination": true,
                "status": "in_use",
                "volume_id": "d-2ze9mho1vp79mctdoro0"
            }
        },
        "eip": {
            "allocation_id": "",
            "internet_charge_type": "",
            "ip_address": ""
        },
        "group_ids": {
            "security_group_id": [
                "sg-2zegcq33l0yz9sknp08o"
            ]
        },
        "host_name": "myhost",
        "id": "i-2ze9zfjdhtasdrfbgay1",
        "image_id": "ubuntu1404_64_40G_cloudinit_20160727.raw",
        "instance_name": "test-instance",
        "instance_type": "ecs.n1.small",
        "io_optimized": true,
        "launch_time": "2017-05-23T00:56Z",
        "private_ip": "10.31.153.209",
        "public_ip": "47.94.45.175",
        "region_id": "cn-beijing",
        "status": "running",
        "tags": {
            "create_test": "0.01"
        },
        "vpc_attributes": {
            "nat_ip_address": "",
            "private_ip_address": {
                "ip_address": []
            },
            "vpc_id": "",
            "vswitch_id": ""
        },
        "zone_id": "cn-beijing-a"
    }
total:
    description: The number of all instances after operating ecs instance.
    returned: when success
    type: int
    sample: 3
failed_instance_ids:
    description: List all instances's id when operating ecs instance is failed.
    returned: 'on join/leave security group'
    type: list
    sample: ["i-35b333d9","i-ddav***"]
group_id:
    description: The security group id that join instance or remove instance.
    returned: 'on join/leave security group'
    type: string
    sample: "sg-35b333d9"
'''

import time
import sys
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import get_acs_connection_info, ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_instance_info(inst):
    """
    Retrieves instance information from an instance
    ID and returns it as a dictionary
    """
    instance_info = {'id': inst.id,
                     'private_ip': inst.inner_ip_address,
                     'public_ip': inst.public_ip_address,
                     'image_id': inst.image_id,
                     'zone_id': inst.zone_id,
                     'region_id': inst.region_id,
                     'launch_time': inst.creation_time,
                     'instance_type': inst.instance_type,
                     'instance_name': inst.instance_name,
                     'host_name': inst.host_name,
                     'group_ids': inst.security_group_ids,
                     'status': inst.status,
                     'tags': inst.tags,
                     'vpc_attributes': inst.vpc_attributes,
                     'eip': inst.eip_address,
                     'io_optimized': inst.io_optimized
                     }
    try:
        bdm_dict = {}
        bdm = getattr(inst, 'block_device_mapping')
        for device_name in bdm.keys():
            bdm_dict[device_name] = {
                'status': bdm[device_name].status,
                'volume_id': bdm[device_name].volume_id,
                'delete_on_termination': bdm[device_name].delete_on_termination
            }
        instance_info['block_device_mapping'] = bdm_dict
    except AttributeError:
        instance_info['block_device_mapping'] = False

    return instance_info


def get_instances(module, ecs, instance_ids):
    """
    get instance info
    module: Ansible module object
    ecs: authenticated ecs connection object
    Returns a dictionary of instance information
    """
    changed = False
    instance_dict_array = []

    if not isinstance(instance_ids, list) or len(instance_ids) < 1:
        module.fail_json(msg='instance_ids should be a list of instances, aborting')
    filters = {}
    # if instance_tags:
    #     for key, value in instance_tags.items():
    #         filters["tag:" + key] = value

    for inst in ecs.get_all_instances(instance_ids=instance_ids):
        instance_dict_array.append(get_instance_info(inst))
        changed = True

    # C2C : Commented printing on to console as it causing error from ansible

    return changed, instance_dict_array, instance_ids


def terminate_instances(module, ecs, instance_ids, instance_tags):
    """
    Terminates a list of instances
    module: Ansible module object
    ecs: authenticated ecs connection object
    termination_list: a list of instances to terminate in the form of
      [ {id: <inst-id>}, ..]
    Returns a dictionary of instance information
    about the instances terminated.
    If the instance to be terminated is running
    "changed" will be set to False.
    """

    changed = False
    instance_dict_array = []

    if not isinstance(instance_ids, list) or len(instance_ids) < 1:
        module.fail_json(msg='instance_ids should be a list of instances, aborting')
    filters = {}
    if instance_tags:
        for key, value in instance_tags.items():
            filters["tag:" + key] = value

    terminated_instance_ids = []
    region, connect_args = get_acs_connection_info(module)
    for inst in ecs.get_all_instances(instance_ids=instance_ids, filters=filters):
        if inst.state == 'absent':
            terminated_instance_ids.append(inst.id)
            instance_dict_array.append(get_instance_info(inst))
            try:
                inst.terminate(**connect_args)
            except ECSResponseError as e:
                module.fail_json(msg='Unable to terminate instance {0}, error: {1}'.format(inst.id, e))
            changed = True

    return changed, instance_dict_array, terminated_instance_ids


def startstop_instances(module, ecs, instance_ids, state, instance_tags):
    """
    Starts, stops or restarts a list of existing instances
    module: Ansible module object
    ecs: authenticated ecs connection object
    instance_ids: The list of instances to start in the form of
      [ "<inst-id>", ..]
    instance_tags: A dict of tag keys and values in the form of
      {key: value, ... }
    state: Intended state ("running" or "stopped")
    Returns a dictionary of instance information
    about the instances started/stopped.
    If the instance was not able to change state,
    "changed" will be set to False.
    Note that if instance_ids and instance_tags are both non-empty,
    this method will process the intersection of the two
    """

    changed = False
    instance_dict_array = []

    if not isinstance(instance_ids, list) or len(instance_ids) < 1:
        # Fail unless the user defined instance tags
        if not instance_tags:
            module.fail_json(msg='instance_ids should be a list of instances, aborting')

    # To make an ECS tag filter, we need to prepend 'tag:' to each key.
    # An empty filter does no filtering, so it's safe to pass it to the
    # get_all_instances method even if the user did not specify instance_tags
    filters = []
    if instance_tags:
        for inst_tag in instance_tags:
            tag = {}
            tag["tag:" + inst_tag['tag_key']] = inst_tag['tag_value']
            filters.append(tag)
    # Check (and eventually change) instances attributes and instances state
    region, connect_args = get_acs_connection_info(module)
    connect_args['force'] = module.params.get('force', None)
    for inst in ecs.get_all_instances(instance_ids=instance_ids, filters=filters):
        if inst.state != state:
            try:
                if state == 'running':
                    inst.start()
                elif state == 'restarted':
                    inst.reboot(force=module.params.get('force', None))
                else:
                    inst.stop(force=module.params.get('force', None))
            except ECSResponseError as e:
                module.fail_json(msg='Unable to change state for instance {0}, error: {1}'.format(inst.id, e))
            changed = True

    for instance_id in instance_ids:
        instance_dict_array.append(get_instance_info(ecs.get_instance_details(instance_id)))

    return changed, instance_dict_array, instance_ids


def delete_instances(module, ecs, instance_ids):
    """
    Delete an ECS Instance
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param instance_ids: The list of instances to delete in the form of
      [ "<inst-id>", ..]
    :return: Id of ECS Instances
    """
    try:
        target = []
        for instance_id in instance_ids:
            instance = ecs.get_instance_details(instance_id=instance_id)
            if str(instance.status) not in ["Stopped", "stopped"]:
                target.append(instance_id)
        startstop_instances(module=module, ecs=ecs, instance_ids=target, state="stopped", instance_tags=None)

        result = ecs.terminate_instances(instance_ids=instance_ids, force=True)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to delete instance, error: {0}'.format(e))

    return result


def create_instance(module, ecs, image_id, instance_type, group_id, zone_id, instance_name, description, internet_data,
                    host_name, password, io_optimized, system_disk, disks, vswitch_id, private_ip, count,
                    allocate_public_ip, bind_eip, instance_charge_type, period, auto_renew, auto_renew_period,
                    instance_tags, ids, wait, wait_timeout):
    """
    create an instance in ecs
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param zone_id: ID of a zone to which an instance belongs. If it is null, a zone is selected by the system
    :param image_id: ID of an image file, indicating an image selected
    when an instance is started
    :param instance_type: Type of the instance
    :param group_id: ID of the security group to which a newly created
        instance belongs
    :param instance_name: Display name of the instance, which is a string
        of 2 to 128 Chinese or English characters. It must begin
        with an uppercase/lowercase letter or a Chinese character
        and can contain numerals, . _ or -
    :param description: Description of the instance, which is a string of
        2 to 256 characters.
    :param internet_data: A hash/dictionaries of internet to the new
        instance
    :param host_name: Host name of the ECS, which is a string of at least
        two characters. hostname cannot start or end with . or -
        In addition, two or more consecutive . or - symbols are
        not allowed.
    :param password: Password to an instance is a string of 8 to 30
        characters
    :param io_optimized: values are :- none: none I/O Optimized and
        optimized: I/O Optimized
    :param system_disk: SystemDisk details of an instance like
        SystemDiskCategory, SystemDiskSize, SystemDiskDiskName
        and SystemDiskDescription
    :param disks: A list of hash/dictionaries of volumes to add to
        the new instance
    :param vswitch_id: When launching an instance in VPC, the virtual
        switch ID must be specified
    :param private_ip: Private IP address of the instance, which cannot be specified separately.
    :param count: The number of the new instance.
    :param allocate_public_ip: Whether allocate a public ip for the
        new instance
    :param bind_eip: An elastic public ip bind to the new instance
    :param instance_charge_type: instance charge type
    :param period: The time that you have bought the resource,in month. Only valid when InstanceChargeType is set as
        PrePaid. Value range: 1 to 12
    :param auto_renew: Whether automatic renewal is supported.
    :param auto_renew_period: The period of each automatic renewal. Required when AutoRenew is True.
        The value must be the same as the period of the created instance.
    :param instance_tags: A list of hash/dictionaries of instance tags,
       '[{tag_key:"value", tag_value:"value"}]', tag_key must be
       not null when tag_value isn't null returns id of newly
       created instance
    :param ids: A list of identifier for this instance or set of
        instances, so that the module will be idempotent with
        respect to ECS instances.
    :param wait: after execution of method whether it has to wait for some time interval
    :param wait_timeout: time interval of waiting
    :return:
        changed: If instance is created successfully the changed will be set
            to True else False
        instance_id: the newly created instance ids
    """

    changed = False
    # check whether the required parameter passed or not
    if not image_id:
        module.fail_json(msg='image_id is required for new instance')
    if not instance_type:
        module.fail_json(msg='instance_type is required for new instance')

    # allow only upto four data_disks or volume
    if disks:
        if len(disks) > 4:
            module.fail_json(msg='more than four volumes or disk are not allowed.')

    # Associating elastic ip binding is not supported for classic n/w type
    if (bind_eip is not None) and (vswitch_id is None):
        module.fail_json(
            msg='associating elastic ip address is not allowed as specified instance is not configured in VPC.')

    # Restrict Instance Count
    if int(count) > 99:
        module.fail_json(
            msg='count value for creating instance is not allowed.')

    # Restrict when length of ids not equal to count
    if ids:
        if len(ids) != count:
            module.fail_json(
                msg='length of ids should be equal to count.')

    try:
        # call to create_instance method from footmark
        changed, instances, result = ecs.create_instance(image_id=image_id, instance_type=instance_type, group_id=group_id,
                                                         zone_id=zone_id, instance_name=instance_name, description=description,
                                                         internet_data=internet_data, host_name=host_name, password=password,
                                                         io_optimized=io_optimized, system_disk=system_disk, disks=disks,
                                                         vswitch_id=vswitch_id, private_ip=private_ip, count=count,
                                                         allocate_public_ip=allocate_public_ip, bind_eip=bind_eip,
                                                         instance_charge_type=instance_charge_type, period=period,
                                                         auto_renew=auto_renew, auto_renew_period=auto_renew_period,
                                                         instance_tags=instance_tags, ids=ids, wait=wait, wait_timeout=wait_timeout)
        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to create instance, error: {0}'.format(e))

    return changed, instances, result


def modify_instance(module, ecs, attributes):
    """
    modify the instance attributes such as name, description, password and host_name

    :param: module: Ansible module object
    :param: ecs: authenticated ecs connection object
    :param: attributes: A list of dictionary of instance attributes which includes
       id, name, description, password and host_name
    :return:
        changed: If instance is modified successfully the changed will be set to True else False
        instance_ids: returns a list of the instance_ids modified
        result: detailed server response
    """
    changed = False
    # check whether the required parameter passed or not
    if attributes:
        for attr in attributes:
            if attr:
                if 'id' not in attr:
                    module.fail_json(msg='instance_id is required for modify instance')
    else:
        module.fail_json(msg='attributes is required for modify instance')

    # call modify_instance method from footmark
    try:
        changed, result = ecs.modify_instance(attributes=attributes)

        instance_ids = []
        for attr in attributes:
            if 'id' in attr:
                instance_ids.append(str(attr['id']))

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)
        changed = True

    except ECSResponseError as e:
        module.fail_json(msg='Unable to modify instance, error: {0}'.format(e))
    return changed, instance_ids, result


def get_instance_status(module, ecs, zone_id=None, pagenumber=None, pagesize=None):
    """
    Get list of instance with their status from zone
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param zone_id: ID of a zone to which an instance belongs.
    :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
    :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50. The default
        value is 10
    :return:
        changed: Changed is always false as there is no change on Aliyun server
        result: detailed server response
    """
    changed = False
    try:
        changed, result = ecs.get_instance_status(zone_id=zone_id, pagenumber=pagenumber, pagesize=pagesize)

        if 'error' in (''.join(str(result))).lower():
            module.fail_json(changed=changed, msg=result)

    except ECSResponseError as e:
        module.fail_json(msg='Unable to get status of instance(s), error: {0}'.format(e))

    return changed, result


def joinleave_security_group(module, ecs, action, instance_ids, security_group_id):
    """
    Instance joins security group id
    :param module: Ansible module object
    :param ecs: authenticated ecs connection object
    :param action: join or leave security group
    :param instance_ids: The list of instance id's which are to be assigned to the security group
    :param security_group_id: ID of the security group to which a instance is to be added
    :return:
        changed: If instance is added successfully in security group. the changed will be set to True else False
        result: detailed server response
    """
    changed = False
    # check whether the required parameter passed or not
    if not instance_ids:
        module.fail_json(msg='instance_id is required to join in new security group or remove from an existing security group.')

    if not isinstance(instance_ids, list):
        module.fail_json(msg='instance_id must be a list')

    if not security_group_id:
        module.fail_json(msg='group_id is required to join in new security group or remove from an existing security group')

    # call join_security_group or leave_security_groupmethod from footmark
    try:
        if action == 'join':
            changed, result, success_instance_ids, failed_instance_ids = \
                ecs.join_security_group(instance_ids, security_group_id)
        else:
            changed, result, success_instance_ids, failed_instance_ids = \
                ecs.leave_security_group(instance_ids, security_group_id)

        if result and 'error' in (''.join(str(result))).lower():
            module.fail_json(msg=result, group_id=security_group_id, instance_ids=success_instance_ids,
                             failed_instance_ids=failed_instance_ids)
    except ECSResponseError as e:
        module.fail_json(msg='Unable to join instance in security group or remove from it, error: {0}'.format(e))
    return changed, result, success_instance_ids, failed_instance_ids, security_group_id


def main():
    if HAS_FOOTMARK is False:
        module.fail_json(msg='footmark required for this module')
    else:
        argument_spec = ecs_argument_spec()
        argument_spec.update(dict(
            group_id=dict(),
            alicloud_zone=dict(aliases=['acs_zone', 'ecs_zone', 'zone_id', 'zone']),
            instance_type=dict(aliases=['type']),
            image_id=dict(aliases=['image']),
            count=dict(type='int', default='1'),
            vswitch_id=dict(aliases=['subnet_id']),
            io_optimized=dict(type='bool', default=False),
            instance_name=dict(),
            internet_data=dict(type='dict'),
            host_name=dict(),
            password=dict(),
            system_disk=dict(type='dict'),
            disks=dict(type='list', aliases=['volumes']),
            force=dict(type='bool', default=False),
            instance_tags=dict(type='list', aliases=['tags']),
            status=dict(default='present', aliases=['state'], choices=['present', 'running', 'stopped', 'restarted',
                                                                       'absent', 'list', 'current']),
            description=dict(),
            allocate_public_ip=dict(type='bool', aliases=['assign_public_ip'], default=True),
            bind_eip=dict(),
            instance_charge_type=dict(default='PostPaid'),
            period=dict(type='int'),
            auto_renew=dict(type='bool', default=False),
            ids=dict(type='list', aliases=['id']),
            attributes=dict(type='list'),
            pagenumber=dict(type='int', default='1'),
            pagesize=dict(type='int', default='10'),
            vpc_id=dict(),
            instance_id=dict(type='list', aliases=['instance_ids']),
            sg_action=dict(),
            private_ip=dict(),
            auto_renew_period=dict(),
            wait=dict(default='no', choices=['yes', 'Yes', 'no', 'No', "True", "False", "true", "false"]),
            wait_timeout=dict(type='int', default='300')
        )
        )
        module = AnsibleModule(argument_spec=argument_spec)

        ecs = ecs_connect(module)
        tagged_instances = []
        status = module.params['status']

        if status == 'absent':
            instance_ids = module.params['instance_id']
            if not isinstance(instance_ids, list) or len(instance_ids) < 1:
                module.fail_json(msg='The parameter instance_ids should be a list, aborting')
            result = delete_instances(module=module, ecs=ecs, instance_ids=instance_ids)
            module.exit_json(changed=True, instance_ids=result, total=len(result))

        elif status in ('running', 'stopped', 'restarted'):
            instance_ids = module.params['instance_ids']
            instance_tags = module.params['instance_tags']
            if not (isinstance(instance_ids, list) or isinstance(instance_tags, list)):
                module.fail_json(
                    msg='running list needs to be a list of instances or set of tags to run: %s' % instance_ids)

            (changed, instance_dict_array, new_instance_ids) = startstop_instances(module, ecs, instance_ids, status,
                                                                                   instance_tags)
            (_, instance_dict_array, new_instance_ids) = get_instances(module, ecs, instance_ids)
            statuses = []
            for inst in instance_dict_array:
                statuses.append(str(inst["status"]))
            module.exit_json(changed=changed, instance_ids=new_instance_ids, instance_statuses=statuses,
                             total=len(new_instance_ids))

        elif status == 'present':
            # Join and leave security group is handled in state present
            # if sg_action parameter is absent then create new instance will begin
            # region Security Group join/leave begin
            sg_action = module.params['sg_action']
            attributes = module.params['attributes']

            if sg_action:
                action = sg_action.strip().lower()

                if action not in ('join', 'leave'):
                    module.fail_json(msg='To perform join_security_group or leave_security_group operation,'
                                         'sg_action must be either join or leave respectively')

                instance_ids = module.params['instance_id']
                security_group_id = module.params['group_id']

                if action == 'join':
                    # Adding an Instance to a Security Group
                    (changed, result, success_instance_ids, failed_instance_ids, security_group_id) = \
                        joinleave_security_group(module, ecs, action, instance_ids, security_group_id)
                else:
                    # Removing an Instance from a Security Group
                    (changed, result, success_instance_ids, failed_instance_ids, security_group_id) = \
                        joinleave_security_group(module, ecs, action, instance_ids, security_group_id)

                (_, instance_dict_array, new_instance_ids) = get_instances(module, ecs, instance_ids)
                statuses = []
                for inst in instance_dict_array:
                    statuses.append(str(inst["status"]))
                module.exit_json(changed=changed, group_id=security_group_id, instance_ids=success_instance_ids,
                                 failed_instance_ids=failed_instance_ids, instance_statuses=statuses,
                                 total=len(new_instance_ids))
            # region Security Group join/leave ends here

            elif attributes:
                # Modifying Instance Attributes
                changed, instance_ids, result = modify_instance(module, ecs, attributes)

                (_, instance_dict_array, new_instance_ids) = get_instances(module, ecs, instance_ids)
                statuses = []
                for inst in instance_dict_array:
                    statuses.append(str(inst["status"]))
                module.exit_json(changed=changed, instance_ids=instance_ids, instance_statuses=statuses,
                                 instances=instance_dict_array, total=len(instance_ids))
            else:
                # Create New Instance
                zone_id = module.params['alicloud_zone']
                image_id = module.params['image_id']
                instance_type = module.params['instance_type']
                group_id = module.params['group_id']
                io_optimized = module.params['io_optimized']
                vswitch_id = module.params['vswitch_id']
                instance_name = module.params['instance_name']
                description = module.params['description']
                internet_data = module.params['internet_data']
                host_name = module.params['host_name']
                password = module.params['password']
                system_disk = module.params['system_disk']
                disks = module.params['disks']
                count = module.params['count']
                allocate_public_ip = module.params['allocate_public_ip']
                bind_eip = module.params['bind_eip']
                instance_tags = module.params['instance_tags']
                period = module.params['period']
                auto_renew = module.params['auto_renew']
                instance_charge_type = module.params['instance_charge_type']
                ids = module.params['ids']
                private_ip = module.params['private_ip']
                auto_renew_period = module.params['auto_renew_period']
                wait = module.params['wait']
                wait_timeout = module.params['wait_timeout']

                changed, instance_list, result = create_instance(module=module, ecs=ecs, image_id=image_id,
                                                                 instance_type=instance_type, group_id=group_id, zone_id=zone_id,
                                                                 instance_name=instance_name, description=description,
                                                                 internet_data=internet_data, host_name=host_name, password=password,
                                                                 io_optimized=io_optimized, system_disk=system_disk, disks=disks,
                                                                 vswitch_id=vswitch_id, private_ip=private_ip, count=count,
                                                                 allocate_public_ip=allocate_public_ip, bind_eip=bind_eip,
                                                                 instance_charge_type=instance_charge_type, period=period,
                                                                 auto_renew=auto_renew, auto_renew_period=auto_renew_period,
                                                                 instance_tags=instance_tags, ids=ids, wait=wait, wait_timeout=wait_timeout)

                instances = []
                instance_ids = []
                statuses = []
                public_ips = []
                for inst in instance_list:
                    instances.append(get_instance_info(inst))
                    instance_ids.append(str(inst.instance_id))
                    statuses.append(str(inst.status))
                    public_ips.append(str(inst.public_ip))
                module.exit_json(changed=changed, instance_ids=instance_ids, instance_statuses=statuses,
                                 instance_ips=public_ips, instances=instances, total=len(instance_list))

        elif status == 'list':
            instance_ids = module.params['instance_ids']

            (changed, instance_dict_array, new_instance_ids) = get_instances(module, ecs, instance_ids)
            statuses = []
            public_ips = []
            for inst in instance_dict_array:
                statuses.append(str(inst["status"]))
                public_ips.append(str(inst["public_ip"]))
            module.exit_json(changed=changed, instance_ids=new_instance_ids, instance_statuses=statuses,
                             instance_ips=public_ips, instances=instance_dict_array, total=len(new_instance_ids))

        elif status == 'current':
            pagenumber = module.params['pagenumber']
            pagesize = module.params['pagesize']
            zone_id = module.params['alicloud_zone']

            (changed, result) = get_instance_status(module, ecs, zone_id, pagenumber, pagesize)

            instance_ids = []
            instance_statuses = []
            for inst in result.instance_statuses['instance_status']:
                instance_ids.append(str(inst["instance_id"]))
                instance_statuses.append(str.lower(str(inst["status"])))
            module.exit_json(changed=changed, instance_ids=instance_ids,
                             instance_statuses=instance_statuses, total=len(instance_ids))

        else:
            module.fail_json(msg='The expected state: {0}, {1}, {2}, {3}, {4}, {5} and {6}, but got {7}.'.format(
                'present', 'running', 'stopped', 'restarted', 'absent', 'list', 'current', status))


if __name__ == '__main__':
    main()

#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com>
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


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ali_ess_configuration
version_added: "1.5.0"
short_description: Create or Terminate an scaling configuration in ESS.
description:
    - Scaling configuration defines the configuration of ECS instances used for Auto Scaling.
      When adding ECS instances to a scaling group, Auto Scaling creates the ECS instances according to the scaling configuration.
options:
    state:
      description:
        - The state of the scaling configuration after operating.
      default: 'present'
      choices: [ 'present', 'active', 'inactive', 'absent' ]
    name:
      description:
        - The name of scaling configuration. The name must contain 2-40 English or Chinese characters,
          and start with a number, a letter in upper or lower case or a Chinese character.
          The name can contain numbers, "_", "-" or ".". Default to configuration Id.
      aliases: ['configuration_name' ]
    image_id:
      description:
        - Image ID used to scale ECS instances. Required when C(state=present).
      aliases: [ 'image' ]
    instance_type:
      description:
        - Instance type used to scale ECS instances. Required when C(state=present).
      aliases: [ 'type' ]
    security_group_id:
      description:
        - Security Group id used to scale ECS instances.
    group_id:
      description:
        - ID of the scaling group of a scaling configuration.
      aliases: [ 'scaling_group_id' ]
    internet_charge_type:
      description:
        - Internet charge type of scaling ECS instance.
      default: "PayByBandwidth"
      choices: ["PayByBandwidth", "PayByTraffic"]
    max_bandwidth_in:
      description:
        - For scaling ECS instance, maximum incoming bandwidth from the public network, measured in Mbps (Mega bit per second).
          Valid values range [1,200].
      default: 200
    max_bandwidth_out:
      description:
        - For scaling ECS instance, maximum outgoing bandwidth to the public network, measured in Mbps (Mega bit per second).
          Valid values range [0,100].
      default: 0
    system_disk_category:
      description:
        - Category of the system disk.
      default: "cloud_efficiency"
      choices: ["cloud_efficiency", "cloud_ssd"]
    system_disk_size:
      description:
        - Size of the system disk, in GB. The valid value range [40, 500]. Default to maximum of specified value and image size.
    id:
      description:
        - The ID of existing scaling configuration.
      aliases: [ 'configuration_id' ]
    data_disks:
      description:
        - List of hash/dictionaries data disks for scaling ECS instances. A maximum of four items can be entered.
      suboptions:
        size:
          description:
            - Size of data disk, in GB. The valid value range [20, 32768]. Ignored when I(snapshot_id).
        category:
          description:
            - Category of data disk.
          default: "cloud_efficiency"
          choices: ["cloud_efficiency", "cloud_ssd"]
        snapshot_id:
          description:
            - Snapshot used for creating the data disk.
        delete_with_instance:
          description:
            - Whether the data disk will be released along with the instance.
          type: bool
          default: True
    tags:
      description:
        - A hash/dictionaries of instance tags, to add to the new instance or for starting/stopping instance by tag. C({"key":"value"})
    key_name:
      description:
        - The name of key pair which is used to access ECS instance in SSH.
      aliases: ['keypair']
    user_data:
      description:
        - User-defined data to customize the startup behaviors of an ECS instance and to pass data into an ECS instance.
          It only will take effect when launching the new ECS instances.
    ram_role_name:
      description:
        - The name of the instance RAM role.
      aliases: ['ram_role']

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark >= 1.3.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# basic provisioning example scaling configuration
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n4.small
    max_bandwidth_out: 10
    system_disk_category: cloud_efficiency
    system_disk_size: 100
    internet_charge_type: PayByBandwidth
    security_group_id: sg-f2rwnfh23r
    group_id: asg-2zebnrbt206pex
    key_name: key-pair-for-ess
    name: configuration-from-ansible
    data_disks:
      - size: 50
        category: cloud_efficiency
      - snapshot_id: s-w3cif22r2rd
        category: cloud_efficiency
    tags:
      CreatedBy: 'Ansible'
      Version: '1'

  tasks:
    - name: launch scaling configuration
      ali_ess_configuration:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        system_disk_category: '{{ system_disk_category }}'
        system_disk_size: '{{ system_disk_size }}'
        instance_type: '{{ instance_type }}'
        internet_charge_type: '{{ internet_charge_type }}'
        max_bandwidth_out: '{{ max_bandwidth_out }}'
        key_name: '{{ key_name }}'
    
    - name: launch scaling configuration with data disks and tags
      ali_ess_configuration:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        image: '{{ image }}'
        system_disk_category: '{{ system_disk_category }}'
        system_disk_size: '{{ system_disk_size }}'
        instance_type: '{{ instance_type }}'
        internet_charge_type: '{{ internet_charge_type }}'
        max_bandwidth_out: '{{ max_bandwidth_out }}'
        key_name: '{{ key_name }}'
        data_disks: '{{ data_disks }}'
        tags: '{{ tags }}'

    - name: delete specified scaling configuration
      ali_ess_configuration:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        name: '{{ image }}'
        state: absent

'''

RETURN = '''
id:
    description: Scaling Configuration ID.
    returned: expect absent
    type: str
    sample: "asc-2zeimuvzeil1ybfd2lt3"
name:
    description: Scaling Configuration name.
    returned: expect absent
    type: str
    sample: ess-configuration-foo
group_id:
    description: ID of the scaling group of a scaling configuration.
    returned: expect absent
    type: str
    sample: "asg-2zeimuvzeil1xfuor9ej"
configuration:
    description: The details of a scaling configuration.
    returned: expect absent
    type: dict
    sample: {
        "creation_time": "2018-01-05T14:03Z",
        "group_id": "asg-2zeimuvzeil1xfuor9ej",
        "id": "asc-2zeimuvzeil1ybfd2lt3",
        "image_id": "centos_6_09_64_20G_alibase_20170825.vhd",
        "instance_type": "ecs.n4.small",
        "name": "test-for-ansible",
        "security_group_id": "sg-2zeb86qfocdo7pvk41tt",
        "status": "inactive"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ess_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_details(configuration):
    return dict(id=configuration.id,
                name=configuration.name,
                group_id=configuration.scaling_group_id,
                status=configuration.status,
                image_id=configuration.image_id,
                instance_type=configuration.instance_type,
                security_group_id=configuration.security_group_id,
                data_disks=getattr(configuration,'data_disks', None),
                creation_time=configuration.creation_time)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(type='str', aliases=['scaling_group_id']),
        instance_type=dict(type='str', aliases=['type']),
        image_id=dict(type='str', aliases=['image']),
        name=dict(type='str', aliases=['configuration_name']),
        internet_charge_type=dict(type='str', default="PayByBandwidth", choices=["PayByBandwidth", "PayByTraffic"]),
        max_bandwidth_in=dict(type='int', default=200),
        max_bandwidth_out=dict(type='int', default=0),
        system_disk_category=dict(type='str', default='cloud_efficiency'),
        system_disk_size=dict(type='int', default='40'),
        tags=dict(type='dict'),
        state=dict(default='present', choices=['present', 'absent']),
        id=dict(type='str', aliases=['configuration_id']),
        key_name=dict(type='str', aliases=['keypair']),
        user_data=dict(type='str'),
        data_disks=dict(type='list'),
        security_group_id=dict(type='str'),
        ram_role_name=dict(type='str', aliases=['ram_role'])
    ))


    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module ali_ess_configuration.")

    ess = ess_connect(module)
    state = module.params['state']
    cfg_id = module.params['id']
    cfg_name = module.params['name']
    scaling_group = module.params['group_id']
    changed = False

    current = None
    all_cfgs = []
    if cfg_id or cfg_name:
        cfgs = ess.describe_configurations(scaling_group_id=scaling_group, scaling_configuration_ids=[cfg_id],
                                           scaling_configuration_names=[cfg_name])

        if cfgs:
            if len(cfgs) > 1:
                for cfg in cfgs:
                    all_cfgs.append(cfg.id)
                module.fail_json(msg="There are several scaling configurations in our record based on name {0}: {1}. "
                                     "Please specified one using 'id' and try again.".format(cfg_name, all_cfgs))
            current = cfgs[0]

    if state == 'present':
        if current is None:
            try:
                data_disks = module.params['data_disks']
                if not isinstance(data_disks, list):
                    module.fail_json(msg="Filed 'data_disks' should be a list, aborting.")

                if not isinstance(module.params['tags'], dict):
                    module.fail_json(msg="Filed 'tags' should be a dict, aborting.")

                current = ess.create_configuration(scaling_group_id=scaling_group,
                                                   image_id=module.params['image_id'],
                                                   instance_type=module.params['instance_type'],
                                                   security_group_id=module.params['security_group_id'],
                                                   name=cfg_name,
                                                   internet_charge_type=module.params['internet_charge_type'],
                                                   max_bandwidth_in=module.params['max_bandwidth_in'],
                                                   max_bandwidth_out=module.params['max_bandwidth_out'],
                                                   system_disk_category=module.params['system_disk_category'],
                                                   system_disk_size=module.params['system_disk_size'],
                                                   data_disks=data_disks,
                                                   tags=module.params['tags'],
                                                   key_pair_name=module.params['key_name'],
                                                   ram_role_name=module.params['ram_role_name'],
                                                   user_data=module.params['user_data'])
                changed = True
            except Exception as e:
                module.fail_json(msg="Create scaling configuration got an error: {0}".format(e))

        module.exit_json(changed=changed, id=current.id, name=current.name, group_id=current.group_id, configuration=get_details(current))

    if current is None:
        if cfg_id or cfg_name:
                module.fail_json(msg="There are no scaling configuration in our record based on id {0} or name {1}. "
                                     "Please check it and try again.".format(cfg_id, cfg_name))
        module.fail_json(msg='Please specify a scaling configuration that you want to terminate by parameters id or name, aborting')

    try:
        module.exit_json(changed=current.terminate())
    except Exception as e:
        module.fail_json(msg='Delete scaling configuration {0} got an error: {1}'.format(current.id, e))


if __name__ == '__main__':
    main()

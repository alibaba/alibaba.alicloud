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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: alicloud_instance
version_added: "2.4"
short_description: Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group.
description:
    - Create, start, stop, restart, modify or terminate ecs instances.
    - Add or remove ecs instances to/from security group.
options:
    state:
      description:
        - The state of the instance after operating.
      default: 'present'
      choices: [ 'present', 'running', 'stopped', 'restarted', 'absent' ]
    alicloud_zone:
      description:
        - Aliyun availability zone ID in which to launch the instance.
          If it is not specified, it will be allocated by system automatically.
      aliases: ['acs_zone', 'ecs_zone', 'zone_id', 'zone' ]
    image_id:
      description: Image ID used to launch instances. Required when C(state=present).
      aliases: [ 'image' ]
    instance_type:
      description: Instance type used to launch instances. Required when C(state=present).
      aliases: [ 'type' ]
    group_id:
      description: Security group id used to launch instance or join/leave existing instances.
      aliases: [ 'security_group_id' ]
    vswitch_id:
      description: The subnet ID in which to launch the instance (VPC).
      aliases: ['subnet_id']
    instance_name:
      description:
        - The name of ECS instance, which is a string of 2 to 128 Chinese or English characters. It must begin with an
          uppercase/lowercase letter or a Chinese character and can contain numerals, ".", "_", or "-".
          It cannot begin with http:// or https://.
      aliases: ['name']
    description:
      description:
        - The description of ECS instance, which is a string of 2 to 256 characters. It cannot begin with http:// or https://.
    internet_charge_type:
      description:
        - Internet charge type, which can be PayByTraffic or PayByBandwidth.
      default: "PayByBandwidth"
      choices: ["PayByBandwidth", "PayByTraffic"]
    max_bandwidth_in:
      description:
        - Maximum incoming bandwidth from the public network, measured in Mbps (Mega bit per second).
      default: 200
      choices: [1~200]
    max_bandwidth_out:
      description:
        - Maximum outgoing bandwidth to the public network, measured in Mbps (Mega bit per second).
      default: 0
      choices: [0~100]
    host_name:
      description: Instance host name.
    password:
      description: The password to login instance.
    disk_category:
      description:
        - Category of the system disk.
      default: "cloud_efficiency"
      choices: ["cloud_efficiency", "cloud_ssd"]
      aliases: ["system_disk_category"]
    disk_size:
      description:
        - Size of the system disk, in GB
      default: 40
      choices: [40~500]
      aliases: ["system_disk_size"]
    disk_name:
      description:
        - Name of a system disk.
      aliases: ["system_disk_name"]
    disk_description:
      description:
        - Description of a system disk.
      aliases: ["system_disk_description"]
    count:
      description: The number of the new instance.
      default: 1
    allocate_public_ip:
      description:
        - Whether allocate a public ip for the new instance.
      default: True
      aliases: [ 'assign_public_ip' ]
      type: bool
    instance_charge_type:
      description:
        - The charge type of the instance.
      choices: ["PrePaid", "PostPaid"]
      default: "PostPaid"
    period:
      description:
        - The charge duration of the instance. Required when C(instance_charge_type="PrePaid").
      choices: [1~9,12,24,36]
      default: 1
    auto_renew:
      description:
        - Whether automate renew the charge of the instance.
      type: bool
      default: False
    auto_renew_period:
      description:
        - The duration of the automatic renew the charge of the instance. Required when C(auto_renew=True).
      choices: [1, 2, 3, 6, 12]
    instance_ids:
      description:
        - A list of instance ids. It is required when need to operate existing instances.
    force:
      description:
        - Whether force to operation. Required when C(state=stopped) or C(state=restarted) or C(state=absent).
      default: False
      type: bool
    instance_tags:
      description:
        - A list of hash/dictionaries of instance tags, '[{tag_key:"value", tag_value:"value"}]',
                    tag_key must be not null when tag_value isn't null
      aliases: ["tags"]
    sg_action:
      description: The action of operating security group.
      choices: ['join', 'leave']
author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 2.6"
    - "footmark"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# basic provisioning example vpc network
- name: basic provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n4.small
    vswitch_id: vsw-abcd1234
    assign_public_ip: True
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
        internet_charge_type: PayByBandwidth
        max_bandwidth_in: 200
        max_bandwidth_out: 50

# advanced example with tagging and host name password
- name: advanced provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n4.small
    group_id: sg-abcd1234
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

# example with system disk configuration
- name: advanced provisioning example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    image: ubuntu1404_64_40G_cloudinit_20160727.raw
    instance_type: ecs.n4.small
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
        disk_category: '{{ disk_category }}'
        disk_size: '{{ disk_size }}'
        disk_name: '{{ disk_name }}'
        disk_description: '{{ disk_description }}'
#
# modifying attributes of ecs instance
#
- name: modify attribute example
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-beijing
    instance_ids: ["i-abcd12346", "i-abcd12345"]
    instance_name: new_name
    password: Passnew123
  tasks:
    - name: modify attribute of multiple instances
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        instance_name: '{{ instance_name }}'
        password: '{{ password }}'
#
# start or terminate instance
#
- name: start or terminate instance
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-shenzhen
    instance_ids: ["i-abcd12346", "i-abcd12345"]
    state: running
  tasks:
    - name: start instance
      alicloud_instance:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        state: '{{ state }}'
#
# stop or restarted instance
#
- name: start stop restart instance
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-shenzhen
    instance_ids: ["i-abcd12346", "i-abcd12345"]
    force: False
    state: restarted
  tasks:
    - name: Restart instance
      ecs:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        state: '{{ state }}'
        force: '{{ force }}'
#
# add an instance to security group
#
- name: Add an instance to security group
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-shenzhen
    instance_ids: ["i-abcd12346", "i-abcd12345"]
    group_id: sg-abcd1234
    sg_action: join
  tasks:
    - name: Add an instance to security group
      ecs:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        group_id: '{{ group_id }}'
        sg_action: '{{ sg_action }}'
#
# remove instance from security group
#
- name: Remove an instance from security group
  hosts: localhost
  vars:
    alicloud_access_key: <your-alicloud-access-key-id>
    alicloud_secret_key: <your-alicloud-access-secret-key>
    alicloud_region: cn-shenzhen
    instance_ids: ["i-abcd12346", "i-abcd12345"]
    group_id: sg-abcd1234
    sg_action: leave
  tasks:
    - name: Remove an instance from security group
      ecs:
        alicloud_access_key: '{{ alicloud_access_key }}'
        alicloud_secret_key: '{{ alicloud_secret_key }}'
        alicloud_region: '{{ alicloud_region }}'
        instance_ids: '{{ instance_ids }}'
        group_id: '{{ group_id }}'
        sg_action: '{{ sg_action }}'
'''

RETURN = '''
instance_ids:
    description: List all instances's id after operating ecs instance.
    returned: expect absent
    type: list
    sample: ["i-35b333d9","i-ddavdaeb3"]
instance_ips:
    description: List all instances's public ip address after operating ecs instance.
    returned: expect absent
    type: list
    sample: ["10.1.1.1","10.1.1.2"]
total:
    description: The number of all instances after operating ecs instance.
    returned: expect absent
    type: int
    sample: 2
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, ecs_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import ECSResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def get_public_ip(instance):
    if instance.public_ip_address:
        return instance.public_ip_address
    elif instance.eip['ip_address']:
        return instance.eip['ip_address']
    return ""


def create_instance(module, ecs):
    """
    create an instance in ecs
    """
    zone_id = module.params['alicloud_zone']
    image_id = module.params['image_id']
    instance_type = module.params['instance_type']
    group_id = module.params['group_id']
    vswitch_id = module.params['vswitch_id']
    instance_name = module.params['instance_name']
    description = module.params['description']
    internet_charge_type = module.params['internet_charge_type']
    max_bandwidth_out = module.params['max_bandwidth_out']
    max_bandwidth_in = module.params['max_bandwidth_out']
    host_name = module.params['host_name']
    password = module.params['password']
    system_disk_category = module.params['disk_category']
    system_disk_size = module.params['disk_size']
    system_disk_name = module.params['disk_name']
    system_disk_description = module.params['disk_description']
    count = module.params['count']
    allocate_public_ip = module.params['allocate_public_ip']
    instance_tags = module.params['instance_tags']
    period = module.params['period']
    auto_renew = module.params['auto_renew']
    instance_charge_type = module.params['instance_charge_type']
    auto_renew_period = module.params['auto_renew_period']

    # check whether the required parameter passed or not
    if not image_id:
        module.fail_json(msg='image_id is required for new instance')
    if not instance_type:
        module.fail_json(msg='instance_type is required for new instance')

    # Restrict Instance Count
    if int(count) > 99:
        module.fail_json(
            msg='count value for creating instance is not allowed.')

    try:
        # call to create_instance method from footmark
        instances = ecs.create_instance(image_id=image_id, instance_type=instance_type, group_id=group_id,
                                        zone_id=zone_id, instance_name=instance_name, description=description,
                                        internet_charge_type=internet_charge_type, max_bandwidth_out=max_bandwidth_out,
                                        max_bandwidth_in=max_bandwidth_in, host_name=host_name, password=password,
                                        io_optimized='optimized', system_disk_category=system_disk_category,
                                        system_disk_size=system_disk_size, system_disk_name=system_disk_name,
                                        system_disk_description=system_disk_description,
                                        vswitch_id=vswitch_id, count=count, allocate_public_ip=allocate_public_ip,
                                        instance_charge_type=instance_charge_type, period=period, auto_renew=auto_renew,
                                        auto_renew_period=auto_renew_period, instance_tags=instance_tags)

    except Exception as e:
        module.fail_json(msg='Unable to create instance, error: {0}'.format(e))

    return instances


def main():
    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for the module alicloud_instance.")

    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(type='str', aliases=['security_group_id']),
        alicloud_zone=dict(type='str', aliases=['acs_zone', 'ecs_zone', 'zone_id', 'zone']),
        instance_type=dict(type='str', aliases=['type']),
        image_id=dict(type='str', aliases=['image']),
        count=dict(type='int', default=1),
        vswitch_id=dict(type='str', aliases=['subnet_id']),
        instance_name=dict(type='str'),
        host_name=dict(type='str'),
        password=dict(type='str', no_log=True),
        internet_charge_type=dict(type='str', default="PayByBandwidth", choices=["PayByBandwidth", "PayByTraffic"]),
        max_bandwidth_in=dict(type='int', default=200),
        max_bandwidth_out=dict(type='int', default=0),
        disk_category=dict(type='str', default='cloud_efficiency', aliases=["system_disk_category"]),
        disk_size=dict(type='int', default='40', aliases=["system_disk_size"]),
        disk_name=dict(type='str', aliases=["system_disk_name"]),
        disk_description=dict(type='str', aliases=["system_disk_description"]),
        force=dict(type='bool', default=False),
        instance_tags=dict(type='list', aliases=['tags']),
        state=dict(default='present', choices=['present', 'running', 'stopped', 'restarted', 'absent']),
        description=dict(type='str'),
        allocate_public_ip=dict(type='bool', aliases=['assign_public_ip'], default=True),
        instance_charge_type=dict(type='str', default='PostPaid'),
        period=dict(type='int', default=1),
        auto_renew=dict(type='bool', default=False),
        instance_ids=dict(type='list'),
        sg_action=dict(type='str'),
        auto_renew_period=dict(type='int'),
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    ecs = ecs_connect(module)
    state = module.params['state']
    instance_ids = module.params['instance_ids']
    zone_id = module.params['alicloud_zone']

    instances = []
    if instance_ids:
        if not isinstance(instance_ids, list):
            module.fail_json(msg='The parameter instance_ids should be a list, aborting')
        instances = ecs.get_all_instances(zone_id=zone_id, instance_ids=instance_ids)

    ids = []
    ips = []
    if state == 'present':
        if len(instances) < 1:
            instances = create_instance(module, ecs)

            for inst in instances:
                ids.append(inst.id)
                ips.append(get_public_ip(inst))
            module.exit_json(changed=True, instance_ids=ids, instance_ips=ips, total=len(ids))

        # Security Group join/leave begin
        sg_action = module.params['sg_action']

        if sg_action:
            action = sg_action.strip().lower()

            if action not in ('join', 'leave'):
                module.fail_json(msg='To perform join_security_group or leave_security_group operation,'
                                     'sg_action must be either join or leave respectively')

            security_group_id = module.params['group_id']
            for inst in instances:
                # Adding an Instance to a Security Group
                if action == 'join':
                    changed = inst.join_security_group(security_group_id)
                else:
                    changed = inst.leave_security_group(security_group_id)

                if inst.id not in ids:
                    ids.append(inst.id)
                ip = get_public_ip(inst)
                if ip not in ips:
                    ips.append(ip)
        # Security Group join/leave ends here

        # Modify instance attribute
        name = module.params['instance_name']
        description = module.params['description']
        host_name = module.params['host_name']
        password = module.params['password']
        for inst in instances:
            update = False
            if name and name != inst.name:
                update = True
            else:
                name = inst.name
            if description and description != inst.description:
                update = True
            else:
                description = inst.description
            if host_name and host_name != inst.host_name:
                update = True
            else:
                host_name = inst.host_name
            if password:
                update = True

            if update:
                try:
                    inst.modify(name=name, description=description, host_name=host_name, password=password)
                except Exception as e:
                    module.fail_json(msg="Modify instance attribute {0} got an error: {1}".format(inst.id, e))

            if inst.id not in ids:
                ids.append(inst.id)
            ip = get_public_ip(inst)
            if ip not in ips:
                ips.append(ip)

        module.exit_json(changed=True, instance_ids=ids, instance_ips=ips, total=len(ids))

    else:
        if len(instances) < 1:
            module.fail_json(msg='Please specify ECS instances that you want to operate by using '
                                 'parameters instance_ids and alicloud_zone, aborting')
        force = module.params['force']
        if state == 'running':
            try:
                for inst in instances:
                    changed = inst.start()
                    if changed:
                        ids.append(inst.id)
                        ips.append(get_public_ip(inst))

                module.exit_json(changed=changed, instance_ids=ids, instance_ips=ips, total=len(ids))
            except Exception as e:
                module.fail_json(msg='Start instances got an error: {0}'.format(e))
        elif state == 'stopped':
            try:
                for inst in instances:
                    changed = inst.stop(force=force)
                    if changed:
                        ids.append(inst.id)
                        ips.append(get_public_ip(inst))

                module.exit_json(changed=changed, instance_ids=ids, instance_ips=ips, total=len(ids))
            except Exception as e:
                module.fail_json(msg='Stop instances got an error: {0}'.format(e))
        elif state == 'restarted':
            try:
                for inst in instances:
                    changed = inst.reboot(force=module.params['force'])
                    if changed:
                        ids.append(inst.id)
                        ips.append(get_public_ip(inst))

                module.exit_json(changed=changed, instance_ids=ids, instance_ips=ips, total=len(ids))
            except Exception as e:
                module.fail_json(msg='Reboot instances got an error: {0}'.format(e))
        else:
            try:
                force = module.params['force']
                for inst in instances:
                    if inst.status is not 'stopped' and not force:
                        module.fail_json(msg="Instance is running, and please stop it or set 'force' as True.")
                    changed = inst.terminate(force=module.params['force'])

                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='Delete instance got an error: {0}'.format(e))


if __name__ == '__main__':
    main()

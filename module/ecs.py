#!/usr/bin/python
# This file is part of Ansible
DOCUMENTATION = '''
---
module: ecs
short_description: create, start, stop, restart or terminate an instance in ecs
common options:
  acs_access_key:
    description: The access key.
    required: false
    default: null
    aliases: []
  acs_secret_access_key:
    description: The access secret key.
    required: false
    default: null
    aliases: []
  state:
    description: The state of the instance after operating.
    required: true
    default: null
    aliases: []
    choices: ['pending', 'running', 'stopped', 'restarted', 'absent'] map operation ['create', 'start', 'stop', 'restart', 'terminate']

function: create instance
  description: create an instance in ecs
  options:
    region:
      description: The Aliyun region ID to use for the instance.
      required: true
      default: null
      aliases: [ 'acs_region', 'ecs_region' ]
    zone:
      description: Aliyun availability zone ID in which to launch the instance
      required: false
      default: null
      aliases: [ 'acs_zone', 'ecs_zone' ]
    image:
      description: Image ID to use for the instance.
      required: true
      default: null
      aliases: []
    instance_type:
      description: Instance type to use for the instance
      required: true
      default: null
      aliases: []
    group_id:
      description: Security group id (or list of ids) to use with the instance
      required: false
      default: null
      aliases: []
    io_optimized:
      description: Whether instance is using optimized volumes.
      required: false
      default: False
      aliases: []
    vswitch_id:
      description: The subnet ID in which to launch the instance (VPC).
      required: false
      default: null
      aliases: []
    instance_name:
      description: Name of the instance to use.
      required: false
      default: null
      aliases: []
    description:
      description: Descripton of the instance to use.
      required: false
      default: null
      aliases: []
    internet_data:
      description:
        - A hash/dictionaries of internet to the new instance;
        - '{"key":"value"}'; keys allowed:
          - charge_type (required:false; default: "PayByBandwidth", choices:["PayByBandwidth", "PayByTraffic"] )
          - max_bandwidth_in(required:false, default:200)
          - max_bandwidth_out(required:false, default:0).
      required: false
      default: null
      aliases: []
    host_name:
      description: Instance host name.
      required: false
      default: null
      aliases: []
    password:
      description: The password to login instance.
      required: false
      default: null
      aliases: []
    system_disk:
      description:
        - A hash/dictionaries of system disk to the new instance;
        - '{"key":"value"}'; keys allowed:
          - disk_category (required:false; default: "cloud"; choices:["cloud", "cloud_efficiency", "cloud_ssd", "ephemeral_ssd"] )
          - disk_size (required:false; default:max{40，ImageSize}; choices:[40~500])
          - disk_name (required:false; default:null)
          - disk_description (required:false; default:null)
      required: false
      default: null
      aliases: []
    volumes:
      description:
        - A list of hash/dictionaries of volumes to add to the new instance;
        - '[{"key":"value", "key":"value"}]'; keys allowed:
          - device_category (required:false; default: "cloud"; choices:["cloud", "cloud_efficiency", "cloud_ssd", "ephemeral_ssd"] )
          - device_size (required:false; default:null; choices:depends on disk_category)
          - device_name (required: false; default:null)
          - device_description (required: false; default:null)
          - delete_on_termination (required:false, default:"true")
          - snapshot (required:false; default:null), volume_type (str), iops (int) - device_type is deprecated use volume_type, iops must be set when volume_type='io1', ephemeral and snapshot are mutually exclusive.
      required: false
      default: null
      aliases: []
    count:
      description: The number of the new instance.
      required: false
      default: 1
      aliases: []
    allocate_public_ip
      description: Whether allocate a public ip for the new instance.
      required: false
      default: true
      aliases: []
    bind_eip:
      description: A list elastic public ips bind to the new instance.
      required:false
      default: null
      aliases: []
    instance_tags:
      description: - A list of hash/dictionaries of instance tags, '[{tag_key:"value", tag_value:"value"}]', tag_key must be not null when tag_value isn't null
      required: false
      default: null
      aliases: []

function: start, stop, restart, terminate instance
  description: start, stop, restart and terminate instancesin ecs
  options:
    instance_ids:
      description: A list of instance ids, currently used for states: running, stopped, restarted, absent
      required: true
      default: null
      aliases: []
    force:
      description: Whether force to operation, currently used fo states: stopped, restarted.
      required: false
      default: False
      aliases: []
    instance_tags:
      description: - A list of hash/dictionaries of instance tags, '[{tag_key:"value", tag_value:"value"}]', tag_key must be not null when tag_value isn't null
      required: false
      default: null
      aliases: []

function: modify instance attribute
  description: modufy instances attributes in ecs
  options:
    attributes:
      description:
        - A list of hash/dictionaries of instance attributes
        - '[{"key":"value", "key":"value"}]', keys allowed:
          - id (required:true; default: null )
          - name (required:false)
          - description (required:false)
          - password (required:false)
          - host_name (required:false)
          - vnc_password (required:false)
      required: false
      default: null
      aliases: []

function: modify instance vpc attribute
  description: modufy instances attributes in ecs
  options:
    vpc_attributes:
      description:
        - A list of hash/dictionaries of instance vpc attributes
        - '[{"key":"value", "key":"value"}]', keys allowed:
          - instance_id (required:true; default: null )
          - vswitch_id (required:false)
          - eip (required)
      required: false
      default: null
      aliases: []

function: modify instance security group attribute
  description: join or leave instances from security group.
  options:
    group_id:
      description: Security group id (or list of ids) to use with the instance
      required: true
      default: null
      aliases: []
    instance_ids:
      description: A list of instance ids.
      required: true
      default: null
      aliases: []
    sg_action:
      description: The action of operating security group.
      required: true
      default: null
      choices: ['join','remove']
      aliases: []
'''


EXAMPLES = '''
- action: modulename opt1=arg1 opt2=arg2

## start or terminate instance
- name: start or terminate instance
  hosts: localhost
  vars:
    acs_access_key: XXXXXXXXXXXXXX
    acs_secret_access_key: XXXXXXXXXXXXXX
    region: cn-shenzhen
    instance_ids: i-94dehop6n
    instance_tags:
    - tag_key: xz_test
      tag_value: '1.20'
    state: running
  tasks:
    - name: start instance
      ecs_model:
        acs_access_key: '{{ acs_access_key }}'
        acs_secret_access_key: '{{ acs_secret_access_key }}'
        region: '{{ region }}'
        instance_ids: '{{ instance_ids }}'
        instance_tags: '{{ instance_tags }}'
        state: '{{ state }}'

## stop or restarted instance
- name: start stop restart instance
  hosts: localhost
  vars:
    acs_access_key: XXXXXXXXXXXXXX
    acs_secret_access_key: XXXXXXXXXXXXXX
    region: cn-shenzhen
    instance_ids: i-94dehop6n
    instance_tags:
    - tag_key: xz_test
      tag_value: '1.20'
    force: False
    state: restarted
  tasks:
    - name: start instance
      ecs_model:
        acs_access_key: '{{ acs_access_key }}'
        acs_secret_access_key: '{{ acs_secret_access_key }}'
        region: '{{ region }}'
        instance_ids: '{{ instance_ids }}'
        instance_tags: '{{ instance_tags }}'
        state: '{{ state }}'

'''

from footmark.exception import ECSResponseError

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
                     'state': inst.state,
                     'tags': inst.tags,
                     'groups': dict((group.id, group.name) for group in inst.groups),
                     'vpc_id': inst.vpc_id,
                     'subnet_id': inst.subnet_id,
                     'vpc_private_ip': inst.vpc_private_ip,
                     'eip': inst.eip,
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

    return (changed, instance_dict_array, terminated_instance_ids)


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
    running_instances_array = []
    region, connect_args = get_acs_connection_info(module)
    connect_args['force'] = module.params.get('force', None)
    for inst in ecs.get_all_instances(instance_ids=instance_ids, filters=filters):
        if inst.state != state:
            instance_dict_array.append(get_instance_info(inst))
            try:
                if state == 'running':
                    inst.start()
                elif state == 'restarted':
                    inst.reboot()
                else:
                    inst.stop()
            except ECSResponseError as e:
                module.fail_json(msg='Unable to change state for instance {0}, error: {1}'.format(inst.id, e))
            changed = True

    return (changed, instance_dict_array, instance_ids)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(type='list'),
        zone_id=dict(aliases=['acs_zone', 'ecs_zone']),
        instance_type=dict(aliases=['type']),
        image_id=dict(),
        count=dict(type='int', default='1'),
        vswitch_id=dict(),
        io_optimized=dict(type='bool', default=False),
        instance_name=dict(),
        internet_data=dict(type='dict'),
        host_name=dict(),
        password=dict(),
        system_disk=dict(type='dict'),
        volumes=dict(type='list'),
        instance_ids=dict(type='list'),
        force=dict(type='bool', default=False),
        instance_tags=dict(type='list'),
        state=dict(default='present', choices=['present', 'running', 'stopped', 'restarted', 'absent']),
    )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    ecs = ecs_connect(module)

    region, acs_connect_kwargs = get_acs_connection_info(module)

    # if region:
    #     try:
    #         vpc = connect_to_aws(boto.vpc, region, **aws_connect_kwargs)
    #     except boto.exception.NoAuthHandlerFound as e:
    #         module.fail_json(msg = str(e))
    # else:
    #     vpc = None

    tagged_instances = []

    state = module.params['state']

    if state == 'absent':
        instance_ids = module.params['instance_ids']
        if not instance_ids:
            module.fail_json(msg='instance_ids list is required for absent state')

        (changed, instance_dict_array, new_instance_ids) = terminate_instances(module, ecs, instance_ids)

    elif state in ('running', 'stopped', 'restarted'):
        instance_ids = module.params['instance_ids']
        instance_tags = module.params['instance_tags']
        if not (isinstance(instance_ids, list) or isinstance(instance_tags, list)):
            module.fail_json(
                msg='running list needs to be a list of instances or set of tags to run: %s' % instance_ids)

        (changed, instance_dict_array, new_instance_ids) = startstop_instances(module, ecs, instance_ids, state,
                                                                               instance_tags)

    elif state == 'present':
        # Changed is always set to true when provisioning new instances
        if not module.params.get('image'):
            module.fail_json(msg='image parameter is required for new instance')

            # if module.params.get('exact_count') is None:
            #     (instance_dict_array, new_instance_ids, changed) = create_instances(module, ecs, vpc)
            # else:
            #     (tagged_instances, instance_dict_array, new_instance_ids, changed) = enforce_count(module, ecs, vpc)

    module.exit_json(changed=changed, instance_ids=new_instance_ids, instances=instance_dict_array,
                     tagged_instances=tagged_instances)


# import module snippets
from ansible.module_utils.basic import *
# from ansible.module_utils.ecs import *
from ecsutils.ecs import *

# import ECSConnection
main()

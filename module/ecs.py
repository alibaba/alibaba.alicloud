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
    zone_id:
      description: Aliyun availability zone ID in which to launch the instance
      required: false
      default: null
      aliases: [ 'acs_zone', 'ecs_zone' ]
    image_id:
      description: Image ID to use for the instance.
      required: true
      default: null
      aliases: []
    instance_type:
      description: Instance type to use for the instance
      required: true
      default: null
      aliases: [ 'type' ]
    group_id:
      description: Security group id to use with the instance
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
      description: ID of Elastic IP Address bind to the new instance.
      required:false
      default: null
      aliases: []
    instance_tags:
      description: - A list of hash/dictionaries of instance tags, '[{tag_key:"value", tag_value:"value"}]', tag_key must be not null when tag_value isn't null
      required: false
      default: null
      aliases: []
    ids:
      description:
        - A list of identifier for this instance or set of instances, so that the module will be idempotent with respect to ECS instances. This identifier should not be reused for another call later on. For details, see the description of client token at U(https://help.aliyun.com/document_detail/25693.html?spm=5176.doc25499.2.7.mrVgE2).
        - The length of the ids is the same with count
      required: false
      default: null
    instance_charge_type:
      description: - The charge type of the instance.
      required: false
      choices:["PrePaid", "PostPaid"]
      default: "PostPaid"
    period:
      description: - The charge duration of the instance, the value is vaild when instance_charge_type is "PrePaid".
      required: false
      choices:[1~9,12,24,36]
      default: null
    auto_renew:
      description: - Whether automate renew the charge of the instance.
      required: false
      choices:[true, false]
      default: false
    auto_renew_period:
      description: - The duration of the automatic renew the charge of the instance. It is vaild when auto_renew is true.
      required: false
      choices:[1, 2, 3, 6, 12]
      default: false


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


import time
from ast import literal_eval

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
                     # 'groups': dict((group.id, group.name) for group in inst.groups),
                     # 'groups': dict((group, group) for group in inst.groups),
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
        # print("inst:====", get_instance_info(inst))
        instance_dict_array.append(get_instance_info(inst))
        changed = True

    # C2C : Commented printing on to console as it causing error from ansible
    #print(instance_dict_array)
    return (changed, instance_dict_array, instance_ids)

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


def create_instance(module, ecs, region, zone_id, image_id, instance_type, group_id, io_optimized,
                    vswitch_id, instance_name, description, internet_data, host_name, password,
                    system_disk, volumes, count, allocate_public_ip, bind_eip, instance_tags):
    """
    create an instance in ecs
    module: Ansible module object
    ecs: authenticated ecs connection object
    region: The instances Region ID
    zone_id: ID of a zone to which an instance belongs. If it is
        null, a zone is selected by the system
    image_id: ID of an image file, indicating an image selected
        when an instance is started
    instance_type: Type of the instance
    group_id: ID of the security group to which a newly created
        instance belongs
    io_optimized: values are :- none: none I/O Optimized and 
        optimized: I/O Optimized
    vswitch_id: When launching an instance in VPC, the virtual
        switch ID must be specified
    instance_name: Display name of the instance, which is a string
        of 2 to 128 Chinese or English characters. It must begin
        with an uppercase/lowercase letter or a Chinese character
        and can contain numerals, . _ or - 
    description: Description of the instance, which is a string of
        2 to 256 characters. 
    internet_data: A hash/dictionaries of internet to the new 
        instance
    host_name: Host name of the ECS, which is a string of at least
        two characters. hostname cannot start or end with . or -
        In addition, two or more consecutive . or - symbols are
        not allowed.
    password: Password to an instance is a string of 8 to 30 
        characters
    system_disk: SystemDisk details of an instance like 
        SystemDiskCategory, SystemDiskSize, SystemDiskDiskName
        and SystemDiskDescription
    volumes: A list of hash/dictionaries of volumes to add to
        the new instance;
    count: The number of the new instance.
    allocate_public_ip: Whether allocate a public ip for the
        new instance
    bind_eip: A list elastic public ips bind to the new instance
    instance_tags: A list of hash/dictionaries of instance tags,
       '[{tag_key:"value", tag_value:"value"}]', tag_key must be
       not null when tag_value isn't null returns id of newly
       created instance
    If instance is created successfully the changed will be set
    to True else False
    """

    changed = False

    # call to CreateInstance method in Footmark
    instance_id = ecs.create_instance(region_id=region, zone_id=zone_id, image_id=image_id,
                                      instance_type=instance_type, group_id=group_id,
                                      io_optimized=io_optimized, vswitch_id=vswitch_id,
                                      instance_name=instance_name, description=description,
                                      internet_data=internet_data, host_name=host_name,
                                      password=password, system_disk=system_disk, volumes=volumes,
                                      count=count, allocate_public_ip=allocate_public_ip,
                                      bind_eip=bind_eip, instance_tags=instance_tags)
    if 'error:' in (''.join(instance_id)).lower():
        module.fail_json(msg='Unable to create new instance in region {0}, {1}'.format(
            region, instance_id))

    changed = True
    return (changed, instance_id)


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        group_id=dict(),
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
        state=dict(default='present', choices=[
                   'present', 'running', 'stopped', 'restarted', 'absent', 'getinfo']),
        description=dict(),
        allocate_public_ip=dict(type='bool', default=True),
        bind_eip=dict(type='list')
    )
    )

    module = AnsibleModule(argument_spec=argument_spec)
    
    ecs = ecs_connect(module)

    region, acs_connect_kwargs = get_acs_connection_info(module)

    # if region:
    # try:
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

    elif state == 'getinfo':
        instance_ids = module.params['instance_ids']
        (changed, instance_dict_array, new_instance_ids) = get_instances(module, ecs, instance_ids)

    elif state == 'present':
        # C2C : Code added to create instance
        region = module.params['region']
        if not region:
            module.fail_json(msg='region is required for new instance')

        zone_id = module.params['zone_id']

        image_id = module.params['image_id']
        if not image_id:
            module.fail_json(msg='image_id is required for new instance')

        instance_type = module.params['instance_type']
        if not instance_type:
            module.fail_json(msg='instance_type is required for new instance')

        group_id = module.params['group_id']
        if not group_id:
            module.fail_json(msg='group_id is required for new instance')

        io_optimized = module.params['io_optimized']
        vswitch_id = module.params['vswitch_id']
        instance_name = module.params['instance_name']
        description = module.params['description']
        internet_data = module.params['internet_data']
        host_name = module.params['host_name']
        password = module.params['password']
        system_disk = module.params['system_disk']
        volumes = module.params['volumes']
        count = module.params['count']
        allocate_public_ip = module.params['allocate_public_ip']
        bind_eip = module.params['bind_eip']
        instance_tags = module.params['instance_tags']

        # allow only upto four datadisks or volume 
        if volumes:
            if len(volumes) > 4:
                module.fail_json(
                    msg='more than four volumes or datadisks are not allowed.') 
        
        if vswitch_id:
            # Allocating public ip is not supported with vpc n/w type
            if allocate_public_ip:
                module.fail_json(
                    msg='allocating public ip address is not allowed as specified instance is configured in VPC.')
        else: 
            # Associating elastic ip binding is not supported for classic n/w type
            if bind_eip:
                module.fail_json(
                    msg='associating elastic ip address is not allowed as specified instance is not configured in VPC.')  
        

        (changed, new_instance_id) = create_instance(module=module, ecs=ecs, region=region,
                                                     zone_id=zone_id, image_id=image_id,
                                                     instance_type=instance_type,
                                                     group_id=group_id, io_optimized=io_optimized,
                                                     vswitch_id=vswitch_id,
                                                     instance_name=instance_name,
                                                     description=description,
                                                     internet_data=internet_data,
                                                     host_name=host_name, password=password,
                                                     system_disk=system_disk, volumes=volumes,
                                                     count=count,
                                                     allocate_public_ip=allocate_public_ip,
                                                     bind_eip=bind_eip,
                                                     instance_tags=instance_tags)
        instance_ids = []
        instance_ids.append(new_instance_id)
        (changed, instance_dict_array, new_instance_id) = get_instances(
            module, ecs, instance_ids)

        module.exit_json(changed=changed, instance_id=new_instance_id,
                         instances_info=instance_dict_array)

    module.exit_json(changed=changed, instance_ids=new_instance_ids, instances=instance_dict_array,
                     tagged_instances=tagged_instances)

# import module snippets
from ansible.module_utils.basic import *
# from ansible.module_utils.ecs import *
from ecsutils.ecs import *
# import ECSConnection
main()
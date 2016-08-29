DOCUMENTATION = '''
---
module: ecs
short_description: create, start, stop, reboot or delete an instance in ecs
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
  stage:
    description: The stage of the instance after operating.
    required: true
    default: null
    aliases: []
    choices: ['pending', 'running', 'stopped', 'restarted', 'deleted'] map operation ['create', 'start', 'stop', 'reboot', 'delete']

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

function: start, stop, reboot, delete instance
  description: start, stop, reboot and delete instancesin ecs
  options:
    instance_ids:
      description: A list of instance ids, currently used for stages: running, stopped, restarted, deleted
      required: true
      default: null
      aliases: []
    force:
      description: Whether force to operation, currently used fo stages: stopped, restarted.
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

## start or delete instance
- name: start or delete instance
  hosts: localhost
  vars: 
    acs_access_key: XXXXXXXXXXXXXX
    acs_secret_access_key: XXXXXXXXXXXXXX
    region: cn-shenzhen
    instance_ids: i-94dehop6n
    instance_tags: 
    - tag_key: xz_test
      tag_value: '1.20'
    stage: running
  tasks:
    - name: start instance
      ecs_model:
        acs_access_key: '{{ acs_access_key }}'
        acs_secret_access_key: '{{ acs_secret_access_key }}'
        region: '{{ region }}'
        instance_ids: '{{ instance_ids }}'
        instance_tags: '{{ instance_tags }}'
        stage: '{{ stage }}'

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
    stage: restarted
  tasks:
    - name: start instance
      ecs_model:
        acs_access_key: '{{ acs_access_key }}'
        acs_secret_access_key: '{{ acs_secret_access_key }}'
        region: '{{ region }}'
        instance_ids: '{{ instance_ids }}'
        instance_tags: '{{ instance_tags }}'
        stage: '{{ stage }}'

'''

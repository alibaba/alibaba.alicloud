DOCUMENTATION = '''
---
module: ecs_ami
short_description: create or destroy an image in ecs
description:
     - Creates or deletes ecs images.
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
    description: create or deregister/delete image
    required: false
    choices: [ "present", "absent" ]
    default: 'present'

function: create image
  description: create an image.
  options:
    instance_id:
      description:
        - instance id of the image to create
      required: false
      default: null
    snapshot_id:
      description:
        - snapshot id of the image to create, image from system of instance
      required: false
      default: null
    name:
      description:
        - The name of the new image to create
      required: false
      default: null
    description:
      description:
        - An optional human-readable string describing the contents and purpose of the AMI.
      required: false
      default: null
    version:
      description:
        - The version of the new image to create.
      required: false
      default: null
    no_reboot:
      description:
        - An optional flag indicating that the bundling process should not attempt to shutdown the instance before bundling. If this flag is True, the responsibility of maintaining file system integrity is left to the owner of the instance. The default choice is "no".
      required: false
      default: no
      choices: [ "yes", "no" ]
    device_mapping:
      version_added: "2.0"
      description:
        - An optional list of device hashes/dictionaries with custom configurations (same block-device-mapping parameters)
        - "Valid properties include: device_name, snapshot_id, size (in GB)".'device_name' choices [/dev/xvda - /dev/xvdz ] 
      required: false
      default: null
    owner_alias:
      description:
        - The owner alias for the new image.
      required: false
      default: null
      choices:['system', 'self', 'others', 'marketplace']
    wait:
      description:
        - wait for the AMI to be in state 'available' before returning.
      required: false
      default: "no"
      choices: [ "yes", "no" ]
    wait_timeout:
      description:
        - how long before wait gives up, in seconds
      default: 300
    tags:
      description:
        - a dictionary of tags to add to the new image; '{"key":"value"}' and '{"key":"value","key":"value"}'
      required: false
      default: null
    launch_permissions:
    description:
      - Users that should be able to launch the ami. Expects dictionary with a key of user_ids. user_ids should be a list of account ids and the number no more than 10.
    required: false
    default: null

function: destroy image
  description: destroy an image.
  options:
    image_id:
      description:
        - Image ID to be deregistered.
      required: true
      default: null
    delete_snapshot:
      description:
        - Whether or not to delete snapshots when deregistering AMI.
      required: false
      default: "no"
      choices: [ "yes", "no" ]
'''

EXAMPLES = '''
# Basic AMI Creation
- ecs_ami:
    acs_access_key: xxxxxxxxxxxxxxxxxxxxxxx
    acs_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    instance_id: i-xxxxxx
    wait: yes
    name: newtest
    tags:
      Name: newtest
      Service: TestService
  register: instance
# Basic AMI Creation, without waiting
- ecs_ami:
    acs_access_key: xxxxxxxxxxxxxxxxxxxxxxx
    acs_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    region: xxxxxx
    snapshot_id: i-xxxxxx
    wait: no
    name: newtest
  register: instance
# AMI Creation, with a custom root-device size and another snapshot attached
- ecs_ami:
    acs_access_key: xxxxxxxxxxxxxxxxxxxxxxx
    acs_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    name: newtest
    device_mapping:
        - device_name: /dev/xvda
          snapshot_id: xxxxxxx
          size: XXX
        - device_name: /dev/xvdb
          snapshot_id: xxxxxxx
          size: YYY
  register: instance
# Deregister/Delete AMI (keep associated snapshots)
- ecs_ami:
    acs_access_key: xxxxxxxxxxxxxxxxxxxxxxx
    acs_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    region: xxxxxx
    image_id: "{{ instance.image_id }}"
    delete_snapshot: False
    state: absent
# Deregister AMI (delete associated snapshots too)
- ecs_ami:
    acs_access_key: xxxxxxxxxxxxxxxxxxxxxxx
    acs_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    region: xxxxxx
    image_id: "{{ instance.image_id }}"
    delete_snapshot: True
    state: absent
# Allow AMI to be launched by another account
- ecs_ami:
    acs_access_key: xxxxxxxxxxxxxxxxxxxxxxx
    acs_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    region: xxxxxx
    image_id: "{{ instance.image_id }}"
    state: present
    launch_permissions:
      user_ids: ['123456789012']
'''
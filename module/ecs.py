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
            except ECSResponseError as e :
                module.fail_json(msg='Unable to change state for instance {0}, error: {1}'.format(inst.id, e))
            changed = True

    return (changed, instance_dict_array, instance_ids)

def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
            group_id = dict(type='list'),
            zone_id = dict(aliases=['acs_zone', 'ecs_zone']),
            instance_type = dict(aliases=['type']),
            image_id = dict(),
            count = dict(type='int', default='1'),
            vswitch_id = dict(),
            io_optimized = dict(type='bool', default=False),
            instance_name = dict(),
            internet_data = dict(type='dict'),
            host_name = dict(),
            password = dict(),
            system_disk = dict(type='dict'),
            volumes = dict(type='list'),
            instance_ids = dict(type='list'),
            force = dict(type='bool', default=False),
            instance_tags = dict(type='list'),
            state = dict(default='present', choices=['present', 'running', 'stopped', 'restarted', 'absent']),
        )
    )

    module = AnsibleModule( argument_spec=argument_spec )

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
            module.fail_json(msg='running list needs to be a list of instances or set of tags to run: %s' % instance_ids)

        (changed, instance_dict_array, new_instance_ids) = startstop_instances(module, ecs, instance_ids, state, instance_tags)

    elif state == 'present':
        # Changed is always set to true when provisioning new instances
        if not module.params.get('image'):
            module.fail_json(msg='image parameter is required for new instance')

        # if module.params.get('exact_count') is None:
        #     (instance_dict_array, new_instance_ids, changed) = create_instances(module, ecs, vpc)
        # else:
        #     (tagged_instances, instance_dict_array, new_instance_ids, changed) = enforce_count(module, ecs, vpc)

    module.exit_json(changed=changed, instance_ids=new_instance_ids, instances=instance_dict_array, tagged_instances=tagged_instances)

# import module snippets
from ansible.module_utils.basic import *
# from ansible.module_utils.ecs import *
from ecsutils.ecs import *
# import ECSConnection
main()
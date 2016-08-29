import time
from ast import literal_eval

from koball.exception import ECSResponseError

# import ecs_util

# try:
#     import boto.ecs
#     from boto.ecs.blockdevicemapping import BlockDeviceType, BlockDeviceMapping
#     from boto.exception import ECSResponseError
#     from boto.vpc import VPCConnection
#     HAS_BOTO = True
# except ImportError:
#     HAS_BOTO = False

def get_instance_info(inst):
    """
    Retrieves instance information from an instance
    ID and returns it as a dictionary
    """
    instance_info = {'id': inst.id,
                     # 'ami_launch_index': inst.ami_launch_index,
                     'inner_ip': inst.inner_ip_address,
                     'public_ip': inst.public_ip_address,
                     'image_id': inst.image_id,
                     'zone_id': inst.zone_id,
                     'region_id': inst.region_id,
                     'launch_time': inst.launch_time,
                     'instance_type': inst.instance_type,
                     'status': inst.status,
                     'tags': inst.tags,
                     # 'groups': dict((group.id, group.name) for group in inst.groups),
                     'groups': dict((group, group) for group in inst.groups),
                     'vpc_id': inst.vpc_id,
                     'vswitch_id': inst.vswitch_id,
                     'private_ip': inst.private_ip_address,
                     'eip': inst.elastic_public_ip,
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

# def create_instances(module, ec2, vpc, override_count=None):
#     """
#     Creates new instances
#     module : AnsibleModule object
#     ec2: authenticated ec2 connection object
#     Returns:
#         A list of dictionaries with instance information
#         about the instances that were launched
#     """

#     group_id = module.params.get('group_id')
#     zone_id = module.params.get('zone')
#     region_id = module.params.get('region')
#     instance_type = module.params.get('instance_type')
#     image_id = module.params.get('image')
#     count = module.params.get('count')
#     user_data = module.params.get('user_data')
#     instance_tags = module.params.get('instance_tags')
#     vpc_vswitch_id = module.params.get('vpc_subnet_id')
#     public_ip = module.boolean(module.params.get('assign_public_ip'))
#     private_ip = module.params.get('private_ip')
#     instance_name = module.params.get('instance_profile_name')
#     volumes = module.params.get('volumes')
#     io_optimized = module.params.get('ebs_optimized')
    
#     vpc_id = None
#     if vpc_vswitch_id:
#         vpc_id = vpc.get_all_subnets(subnet_ids=[vpc_subnet_id])[0].vpc_id

#     try:
#         if group_id:
#             #wrap the group_id in a list if it's not one already
#             if isinstance(group_id, basestring):
#                 group_id = [group_id]
#             grp_details = ec2.get_all_security_groups(group_ids=group_id)
#             group_name = [grp_item.name for grp_item in grp_details]
#     except boto.exception.NoAuthHandlerFound as e:
#             module.fail_json(msg = str(e))

#     # Lookup any instances that much our run id.

#     running_instances = []
#     count_remaining = int(count)

#     if id != None:
#         filter_dict = {'client-token':id, 'instance-stage-name' : 'running'}
#         previous_reservations = ec2.get_all_instances(None, filter_dict)
#         for res in previous_reservations:
#             for prev_instance in res.instances:
#                 running_instances.append(prev_instance)
#         count_remaining = count_remaining - len(running_instances)

#     # Both min_count and max_count equal count parameter. This means the launch request is explicit (we want count, or fail) in how many instances we want.

#     if count_remaining == 0:
#         changed = False
#     else:
#         changed = True
#         try:
#             params = {'region_id': region_id,
#                       'image_id': image,
#                       'instance_type': instance_type,
#                       'securitygroup_id': group_id}

#             if zone

#             if ebs_optimized:
#               params['ebs_optimized'] = ebs_optimized

#             # 'tenancy' always has a default value, but it is not a valid parameter for spot instance resquest
#             if not spot_price:
#               params['tenancy'] = tenancy

#             if boto_supports_profile_name_arg(ec2):
#                 params['instance_profile_name'] = instance_profile_name
#             else:
#                 if instance_profile_name is not None:
#                     module.fail_json(
#                         msg="instance_profile_name parameter requires Boto version 2.5.0 or higher")

#             if assign_public_ip:
#                 if not boto_supports_associate_public_ip_address(ec2):
#                     module.fail_json(
#                         msg="assign_public_ip parameter requires Boto version 2.13.0 or higher.")
#                 elif not vpc_subnet_id:
#                     module.fail_json(
#                         msg="assign_public_ip only available with vpc_subnet_id")

#                 else:
#                     if private_ip:
#                         interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(
#                             subnet_id=vpc_subnet_id,
#                             private_ip_address=private_ip,
#                             groups=group_id,
#                             associate_public_ip_address=assign_public_ip)
#                     else:
#                         interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(
#                             subnet_id=vpc_subnet_id,
#                             groups=group_id,
#                             associate_public_ip_address=assign_public_ip)
#                     interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)
#                     params['network_interfaces'] = interfaces
#             else:
#                 if network_interfaces:
#                     if isinstance(network_interfaces, basestring):
#                         network_interfaces = [network_interfaces]
#                     interfaces = []
#                     for i, network_interface_id in enumerate(network_interfaces):
#                         interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(
#                             network_interface_id=network_interface_id,
#                             device_index=i)
#                         interfaces.append(interface)
#                     params['network_interfaces'] = \
#                         boto.ec2.networkinterface.NetworkInterfaceCollection(*interfaces)
#                 else:
#                     params['subnet_id'] = vpc_subnet_id
#                     if vpc_subnet_id:
#                         params['security_group_ids'] = group_id
#                     else:
#                         params['security_groups'] = group_name

#             if volumes:
#                 bdm = BlockDeviceMapping()
#                 for volume in volumes:
#                     if 'device_name' not in volume:
#                         module.fail_json(msg = 'Device name must be set for volume')
#                     # Minimum volume size is 1GB. We'll use volume size explicitly set to 0
#                     # to be a signal not to create this volume
#                     if 'volume_size' not in volume or int(volume['volume_size']) > 0:
#                         bdm[volume['device_name']] = create_block_device(module, ec2, volume)

#                 params['block_device_map'] = bdm

#             # check to see if we're using spot pricing first before starting instances
#             if not spot_price:
#                 if assign_public_ip and private_ip:
#                     params.update(dict(
#                       min_count          = count_remaining,
#                       max_count          = count_remaining,
#                       client_token       = id,
#                       placement_group    = placement_group,
#                     ))
#                 else:
#                     params.update(dict(
#                       min_count          = count_remaining,
#                       max_count          = count_remaining,
#                       client_token       = id,
#                       placement_group    = placement_group,
#                       private_ip_address = private_ip,
#                     ))

#                 # Spot instances do not support start/stop thereby not having the option to change shutdown behavior
#                 params['instance_initiated_shutdown_behavior'] = instance_initiated_shutdown_behavior

#                 res = ec2.run_instances(**params)
#                 instids = [ i.id for i in res.instances ]
#                 while True:
#                     try:
#                         ec2.get_all_instances(instids)
#                         break
#                     except boto.exception.EC2ResponseError as e:
#                         if "<Code>InvalidInstanceID.NotFound</Code>" in str(e):
#                             # there's a race between start and get an instance
#                             continue
#                         else:
#                             module.fail_json(msg = str(e))

#                 # The instances returned through ec2.run_instances above can be in
#                 # terminated action due to idempotency. See commit 7f11c3d for a complete
#                 # explanation.
#                 terminated_instances = [
#                     str(instance.id) for instance in res.instances if instance.stage == 'terminated'
#                 ]
#                 if terminated_instances:
#                     module.fail_json(msg = "Instances with id(s) %s " % terminated_instances +
#                                            "were created previously but have since been terminated - " +
#                                            "use a (possibly different) 'instanceid' parameter")

#             else:
#                 if private_ip:
#                     module.fail_json(
#                         msg='private_ip only available with on-demand (non-spot) instances')
#                 if boto_supports_param_in_spot_request(ec2, 'placement_group'):
#                     params['placement_group'] = placement_group
#                 elif placement_group :
#                         module.fail_json(
#                             msg="placement_group parameter requires Boto version 2.3.0 or higher.")

#                 if boto_supports_param_in_spot_request(ec2, 'instance_initiated_shutdown_behavior'):
#                     params['instance_initiated_shutdown_behavior'] = instance_initiated_shutdown_behavior
#                 elif instance_initiated_shutdown_behavior:
#                     module.fail_json(
#                         msg="instance_initiated_shutdown_behavior parameter is not supported by your Boto version.")

#                 if spot_launch_group and isinstance(spot_launch_group, basestring):
#                     params['launch_group'] = spot_launch_group

#                 params.update(dict(
#                     count = count_remaining,
#                     type = spot_type,
#                 ))
#                 res = ec2.request_spot_instances(spot_price, **params)

#                 # Now we have to do the intermediate waiting
#                 if wait:
#                     spot_req_inst_ids = dict()
#                     spot_wait_timeout = time.time() + spot_wait_timeout
#                     while spot_wait_timeout > time.time():
#                         reqs = ec2.get_all_spot_instance_requests()
#                         for sirb in res:
#                             if sirb.id in spot_req_inst_ids:
#                                 continue
#                             for sir in reqs:
#                                 if sir.id == sirb.id and sir.instance_id is not None:
#                                     spot_req_inst_ids[sirb.id] = sir.instance_id
#                         if len(spot_req_inst_ids) < count:
#                             time.sleep(5)
#                         else:
#                             break
#                     if spot_wait_timeout <= time.time():
#                         module.fail_json(msg = "wait for spot requests timeout on %s" % time.asctime())
#                     instids = spot_req_inst_ids.values()
#         except boto.exception.BotoServerError as e:
#             module.fail_json(msg = "Instance creation failed => %s: %s" % (e.error_code, e.error_message))

#         # wait here until the instances are up
#         num_running = 0
#         wait_timeout = time.time() + wait_timeout
#         while wait_timeout > time.time() and num_running < len(instids):
#             try:
#                 res_list = ec2.get_all_instances(instids)
#             except boto.exception.BotoServerError as e:
#                 if e.error_code == 'InvalidInstanceID.NotFound':
#                     time.sleep(1)
#                     continue
#                 else:
#                     raise

#             num_running = 0
#             for res in res_list:
#                 num_running += len([ i for i in res.instances if i.stage=='running' ])
#             if len(res_list) <= 0:
#                 # got a bad response of some sort, possibly due to
#                 # stale/cached data. Wait a second and then try again
#                 time.sleep(1)
#                 continue
#             if wait and num_running < len(instids):
#                 time.sleep(5)
#             else:
#                 break

#         if wait and wait_timeout <= time.time():
#             # waiting took too long
#             module.fail_json(msg = "wait for instances running timeout on %s" % time.asctime())

#         #We do this after the loop ends so that we end up with one list
#         for res in res_list:
#             running_instances.extend(res.instances)

#         # Enabled by default by AWS
#         if source_dest_check is False:
#             for inst in res.instances:
#                 inst.modify_attribute('sourceDestCheck', False)

#         # Disabled by default by AWS
#         if termination_protection is True:
#             for inst in res.instances:
#                 inst.modify_attribute('disableApiTermination', True)

#         # Leave this as late as possible to try and avoid InvalidInstanceID.NotFound
#         if instance_tags:
#             try:
#                 ec2.create_tags(instids, instance_tags)
#             except boto.exception.EC2ResponseError as e:
#                 module.fail_json(msg = "Instance tagging failed => %s: %s" % (e.error_code, e.error_message))

#     instance_dict_array = []
#     created_instance_ids = []
#     for inst in running_instances:
#         inst.update()
#         d = get_instance_info(inst)
#         created_instance_ids.append(inst.id)
#         instance_dict_array.append(d)

#     return (instance_dict_array, created_instance_ids, changed)

def terminate_instances(module, ecs, instance_ids, instance_tags):
    """
    Terminates a list of instances
    module: Ansible module object
    ec2: authenticated ec2 connection object
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
    # for res in ec2.get_all_instances(instance_ids):
    for inst in ec2.get_all_instances(instance_ids=instance_ids, filters=filters):
        if inst.status.lower() == 'deleted':
            terminated_instance_ids.append(inst.id)
            instance_dict_array.append(get_instance_info(inst))
            try:
                inst.delete(**connect_args)
            except ECSResponseError as e:
                module.fail_json(msg='Unable to terminate instance {0}, error: {1}'.format(inst.id, e))
            changed = True

    return (changed, instance_dict_array, terminated_instance_ids)

def startstop_instances(module, ecs, instance_ids, stage, instance_tags):
    """
    Starts, stops or restarts a list of existing instances 
    module: Ansible module object
    ecs: authenticated ecs connection object
    instance_ids: The list of instances to start in the form of
      [ "<inst-id>", ..]
    instance_tags: A dict of tag keys and values in the form of
      {key: value, ... }
    stage: Intended stage ("running" or "stopped")
    Returns a dictionary of instance information
    about the instances started/stopped.
    If the instance was not able to change stage,
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
    # Check (and eventually change) instances attributes and instances stage
    running_instances_array = []
    region, connect_args = get_acs_connection_info(module)
    connect_args['force'] = module.params.get('force', None)
    # for inst in ecs.get_all_instances(instance_ids, filters=filters):
    for inst in ecs.get_all_instances(instance_ids=instance_ids, filters=filters):
        if inst.status.lower() != stage:
            instance_dict_array.append(get_instance_info(inst))
            try:
                if stage == 'running':
                    inst.start(**connect_args)
                elif stage == 'restarted':
                    inst.reboot(**connect_args)
                else: 
                    inst.stop(**connect_args)
            except ECSResponseError as e :
                module.fail_json(msg='Unable to change stage for instance {0}, error: {1}'.format(inst.id, e))
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
            stage = dict(default='pending', choices=['pending', 'running', 'stopped', 'restarted', 'deleted']),
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

    stage = module.params['stage']

    if stage == 'deleted':
        instance_ids = module.params['instance_ids']
        if not instance_ids:
            module.fail_json(msg='instance_ids list is required for absent stage')

        (changed, instance_dict_array, new_instance_ids) = terminate_instances(module, ecs, instance_ids)

    elif stage in ('running', 'stopped', 'restarted'):
        instance_ids = module.params['instance_ids']
        instance_tags = module.params['instance_tags']
        if not (isinstance(instance_ids, list) or isinstance(instance_tags, list)):
            module.fail_json(msg='running list needs to be a list of instances or set of tags to run: %s' % instance_ids)

        (changed, instance_dict_array, new_instance_ids) = startstop_instances(module, ecs, instance_ids, stage, instance_tags)

    elif stage == 'pending':
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
from ansible.module_utils.ecs import *
# import ECSConnection
main()
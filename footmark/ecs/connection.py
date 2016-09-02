# encoding: utf-8
"""
Represents a connection to the ECS service.
"""

import base64
import warnings
from datetime import datetime
from datetime import timedelta

from aliyunsdkecs.request.v20140526.DeleteInstanceRequest import DeleteInstanceRequest

import footmark
from footmark.connection import ACSQueryConnection
from footmark.ecs.instance import *
from footmark.ecs.regioninfo import RegionInfo
from footmark.exception import ECSResponseError
import six

class ECSConnection(ACSQueryConnection):


    # SDKVersion = footmark.config.get('Footmark', 'ecs_version', '2014-05-26')
    SDKVersion = '2014-05-26'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    ResponseError = ECSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version= None, security_token=None,):
        """
        Init method to create a new connection to ECS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.ECSSDK = 'aliyunsdkecs.request.v' + self.SDKVersion.replace('-','')

        super(ECSConnection, self).__init__(acs_access_key_id,
                                            acs_secret_access_key,
                                            self.region, self.ECSSDK, security_token)

    # def build_filter_params(self, params, filters):
    #     if not isinstance(filters, dict):
    #         filters = dict(filters)
    #
    #     i = 1
    #     for name in filters:
    #         acs_name = name
    #         if acs_name.startswith('tag:'):
    #             params['set_Tag%dKey' % i] = acs_name[4:]
    #             params['set_Tag%dValue' % i] = filters[acs_name]
    #             i += 1
    #             continue
    #         acs_name = ''.join(s.capitalize() for s in acs_name.split('_'))
    #         params['set_' + acs_name] = filters[name]

    def build_filter_params(self, params, filters):
        if not isinstance(filters, dict):
            filters = dict(filters)

        i = 1
        for key,value in filters.items():
            acs_key = key
            if acs_key.startswith('tag:'):
                while(('set_Tag%dKey' % i) in params ):
                    i += 1
                if i<6:
                    params['set_Tag%dKey' % i] = acs_key[4:]
                    params['set_Tag%dValue' % i] = filters[acs_key]
                i += 1
                continue
            if not isinstance(value, dict):
                acs_key = ''.join(s.capitalize() for s in acs_key.split('_'))
                params['set_' + acs_key] = value
                continue

            self.build_filters_params(params, value)

    # Instance methods

    def get_all_instances(self, instance_ids=None, filters=None, max_results=None):
        """
        Retrieve all the instance associated with your account.

        :rtype: list
        :return: A list of  :class:`footmark.ecs.instance.Reservation`

        """
        warnings.warn(('The current get_all_instances implementation will be '
                       'replaced with get_all_reservations.'),
                      PendingDeprecationWarning)
        # return self.get_all_reservations(instance_ids=instance_ids,
        #                                  filters=filters, dry_run=dry_run,
        #                                  max_results=max_results)

        params = {}
        if instance_ids:
            self.build_list_params(params, instance_ids, 'InstanceIds')
        if filters:
            if 'group-id' in filters:
                gid = filters.get('group-id')
                if not gid.startswith('sg-') or len(gid) != 12:
                    warnings.warn(
                        "The group-id filter now requires a security group "
                        "identifier (sg-*) instead of a group name. To filter "
                        "by group name use the 'group-name' filter instead.",
                        UserWarning)
                params['set_SecurityGroupId'] = gid
            self.build_filter_params(params, filters)
        if max_results is not None:
            params['MaxResults'] = max_results
        return self.get_list('DescribeInstances', params, ['Instances', Instance])

    def start_instances(self, instance_ids=None):
        """
        Start the instances specified

        :type instance_ids: list
        :param instance_ids: A list of strings of the Instance IDs to start

        :type dry_run: bool
        :param dry_run: Set to True if the operation should not actually run.

        :rtype: list
        :return: A list of the instances started
        """
        params = {}
        results = []
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                self.build_list_params(params, instance_id, 'InstanceId')
                results.append(self.get_list('StartInstance', params, [(self, self)]))
        return results

    def stop_instances(self, instance_ids=None, force=False):
        """
        Stop the instances specified

        :type instance_ids: list
        :param instance_ids: A list of strings of the Instance IDs to stop

        :type force: bool
        :param force: Forces the instance to stop

        :type dry_run: bool
        :param dry_run: Set to True if the operation should not actually run.

        :rtype: list
        :return: A list of the instances stopped
        """
        params = {}
        results = []
        if force:
            self.build_list_params(params, 'true', 'ForceStop')
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                self.build_list_params(params, instance_id, 'InstanceId')
                results.append(self.get_list('StopInstance', params, [(self, self)]))
        return results

    def reboot_instances(self, instance_ids=None, force=False):
        """
        Reboot the specified instances.

        :type instance_ids: list
        :param instance_ids: The instances to terminate and reboot

        :type dry_run: bool
        :param dry_run: Set to True if the operation should not actually run.

        """
        params = {}
        results = []
        if force:
            self.build_list_params(params, 'true', 'ForceStop')
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                self.build_list_params(params, instance_id, 'InstanceId')
                results.append(self.get_list('RebootInstance', params, None))
        return results

    def run_instances(self, **kwargs):
        """

        :rtype: Instance
        :return: The :class:`boto.ec2.instance.Reservation` associated with
                 the request for machines
        """
        params = {}
        if len(kwargs)>0:
            self.build_filter_params(params, kwargs)
        # if 'count' in kwargs and kwargs['count']>0:
        #     for i in range(0,int(kwargs['count']))

        return self.get_object('CreateInstance', params, Instance)
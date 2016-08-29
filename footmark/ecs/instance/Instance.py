#coding=UTF-8
from aliyunsdkcore import client

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeTagsRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import RebootInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from six.moves import configparser
from collections import defaultdict

from footmark.exception import *

class Instance(object):
    def __init__(self):
        # The unique ID of the Instance.
        self.id = ''
        # A list of Group objects representing the security groups associated with the instance.
        self.groups = []
        # The public IP address of the instance.
        self.public_ip_address = ''
        # The inner IP address of the instance.
        self.inner_ip_address = ''
        # The string representation of the instance’s current status.
        self.status = ''
        # The type of instance (e.g. m1.small).
        self.instance_type = ''
        # The time the instance was launched.
        self.launch_time = ''
        # The ID of the AMI used to launch this instance.
        self.image_id = ''
        # The region in which the instance is running.
        self.region_id = ''
        # The availability zone in which the instance is running.
        self.zone_id = ''
        # The kernel associated with the instance.
        self.vswitch_id = ''
        # The VPC ID, if running in VPC.
        self.vpc_id = ''
        # The private IP address of the instance.
        self.private_ip_address = ''
        # The public IP address of the instance.
        self.elastic_public_ip = ''
        # Whether instance is using optimized EBS volumes or not.
        self.io_optimized = ''
        # Tags of the instance
        self.tags = {}

    def __connect__(self, **connect_args):
        try:
            conn = client.AcsClient(connect_args.get('acs_access_key'), connect_args.get('acs_secret_access_key'), self.region_id)
            if not conn:
                raise ACSConnectionError('Connect to ACSClient error, connection is %s' % conn)
            return conn
        except:
            raise

    def start(self, **connect_args):
        try: 
            conn = self.__connect__(**connect_args)
            request = StartInstanceRequest.StartInstanceRequest()
            request.set_accept_format('json')
            request.set_InstanceId(self.id)
            response = conn.get_response(request)
            if not response[0] in (200, 201):
                raise ECSResponseError(response[0], body = response[-1])
        except:
            pass


    def stop(self, **connect_args):
        try:
            conn = self.__connect__(**connect_args)
            request = StopInstanceRequest.StopInstanceRequest()
            request.set_accept_format('json')
            request.set_InstanceId(self.id)
            if connect_args.get('force'):
                request.set_ForceStop(connect_args.get('force'))
            response = conn.get_response(request)
            if not response[0] in (200, 201):
                raise ECSResponseError(response[0], body = response[-1])
        except:
            raise

    def reboot(self, **connect_args):
        try:
            conn = self.__connect__(**connect_args)
            request = RebootInstanceRequest.RebootInstanceRequest()
            request.set_accept_format('json')
            request.set_InstanceId(self.id)
            if connect_args.get('force'):
                request.set_ForceStop(connect_args.get('force'))
            response = conn.get_response(request)
            if not response[0] in (200, 201):
                raise ECSResponseError(response[0], body = response[-1])
        except:
            raise

    def delete(self, **connect_args):
        try:
            conn = self.__connect__(**connect_args)
            request = DeleteInstanceRequest.DeleteInstanceRequest()
            request.set_accept_format('json')
            request.set_InstanceId(self.id)
            response = conn.get_response(request)
            if not response[0] in (200, 201):
                raise ECSResponseError(response[0], body = response[-1])
        except:
            raise

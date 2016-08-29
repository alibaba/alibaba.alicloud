from aliyunsdkcore import client

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeTagsRequest
from six.moves import configparser
from collections import defaultdict

from footmark.ecs.instance.Instance import *
try:
    import json
except ImportError:
    import simplejson as json

class ECSConnection:
    def __init__(self, acs_access_key, acs_secret_access_key, region, security_token):
        self.acs_access_key = acs_access_key
        self.acs_secret_access_key = acs_secret_access_key
        self.region = region
        self.security_token = security_token
        self.__conn = client.AcsClient(self.acs_access_key, self.acs_secret_access_key, self.region)

    def get_all_instances(self, instance_ids=None, filters=None, dry_run=False, max_results=None):
        all_instances = []
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        if instance_ids:
            request.set_InstanceIds(str(instance_ids))
        if filters:
            all_filter = []
            all_tags = []
            tag = {}
            for filt in filters:
                for k,v in filt.items():
                    cur = 1
                    if k.strip().startswith('tag:'):
                        key = k[4:]
                        if cur==1:
                            request.set_Tag1Key(key)
                            request.set_Tag1Value(v)
                        elif cur==2:
                            request.set_Tag2Key(key)
                            request.set_Tag2Value(v)
                        elif cur==3:
                            request.set_Tag3Key(key)
                            request.set_Tag3Value(v)
                        elif cur==4:
                            request.set_Tag4Key(key)
                            request.set_Tag4Value(v)
                        elif cur==5:
                            request.set_Tag5Key(key)
                            request.set_Tag5Value(v)
                        cur = cur + 1
        if dry_run:
            request.set_Status('Running')
        reservations = []
        if max_results:
            page_number = 100
            page = max_results / page_number
            if page == 0:
                page = 1
                page_number = max_results
            for cur in range(1,page+1):
                true_request = request
                true_request.set_PageSize(cur)
                true_request.set_PageNumber(page_number)
                try:
                    instances = json.loads(self.__conn.do_action(true_request)).get('Instances').get('Instance')
                    reservations.extend(instances)
                except:
                    raise
        else:
            try:
                reservations.extend(json.loads(self.__conn.do_action(request)).get('Instances').get('Instance'))
            except:
                raise
        for instance in reservations:
            all_instances.append(self.__parse_DescribeInstances(instance))
        return all_instances

    def __parse_DescribeInstances(self, instance):
        new_instance = Instance()
        if instance is None or len(instance)<1:
            return None
        new_instance.id = instance.get('InstanceId')
        new_instance.groups = [x for x in instance.get('SecurityGroupIds').get('SecurityGroupId')]
        new_instance.public_ip_address = "".join(instance.get('PublicIpAddress').get('IpAddress'))
        new_instance.inner_ip_address = "".join(instance.get('InnerIpAddress').get('IpAddress'))
        new_instance.status = instance.get('Status')
        new_instance.instance_type = instance.get('InstanceType')
        new_instance.launch_time = instance.get('CreationTime')
        new_instance.image_id = instance.get('ImageId')
        new_instance.region_id = instance.get('RegionId')
        new_instance.zone_id = instance.get('ZoneId')
        new_instance.vswitch_id = instance.get('VpcAttributes').get('VSwitchId')
        new_instance.vpc_id = instance.get('VpcAttributes').get('VpcId')
        new_instance.private_ip_address = "".join(x for x in instance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress'))
        new_instance.elastic_public_ip = instance.get('EipAddress').get('IpAddress')
        new_instance.io_optimized = instance.get('IoOptimized')
        tags = instance.get('Tags')
        new_tag = {}
        if tags:
            for tag in tags['Tag']:
                new_tag[tag.get('TagKey')] = tag.get('TagValue')
        new_instance.tags = new_tag
        return new_instance

# ECSConnection()

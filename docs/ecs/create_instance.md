# ECS - Creating an instance

* [Synopsis](#synopsis)
* [Requirements](#requirements)
* [Options](#options)
* [Examples](#examples)
* [Notes](#notes)
* Module Status: **stableinterface**
* This is module is supported by: **core**

## Synopsis
* Creates an elastic compute instances.

## Requirements
  On host that executes module.
 
* Python 2.7.X
* The latest stable release of Ansible
* aliyun-python-sdk-core, aliyun-python-sdk-ecs, ecsutils and footmark Python Packages

## Options

| Parameter	               | Type	       | Required    | Default        |   Choice	                 |   Description   |
|----------------------    |---	           |---	         |---	          |---                           |---              |  
| acs_access_key           | String        |   Yes	     |   	          |   	                         | Aliyun Cloud access key. If not set then the value of the `ACS_ACCESS_KEY_ID`, `ACS_ACCESS_KEY` or `ECS_ACCESS_KEY` environment variable is used.<br/><br/>aliases: `ecs_secret_key`, `secret_key` |
| acs_secret_access_key    | String        |   Yes	     |   	          |   	                         | Aliyun Cloud secret key. If not set then the value of the `ACS_SECRET_ACCESS_KEY`, `ACS_SECRET_KEY`, or `ECS_SECRET_KEY` environment variable is used.<br/><br/>aliases: `ecs_access_key`, `access_key` |
| state                    | String        |   Yes	     |   	          |   	                         | For creating new instance provide state as **present** |
| region                   | String        |   Yes	     |   	          |   	                         | The Aliyun Cloud region to use. If not specified then the value of the `ACS_REGION`, `ACS_DEFAULT_REGION` or `ECS_REGION` environment variable, if any, is used.|
| zone_id                  | String        |   No	     |   	          |   	                         | ID of a zone to which an instance belongs. If it is null, a zone is selected by the system. |
| image_id                 | String        |   Yes	     |   	          |   	                         | ID of an image to use for creating new ECS instance. |
| instance_type            | String        |   No        |                |                              | instance type to use for the instance, see https://intl.aliyun.com/help/doc-detail/25685.htm|
| group_id                 | String        |   No        |                |                              | ID of the security group to which a newly created instance belongs. If not specified, the newly created instance will be added to the default security group. If the default group doesn’t exist, or the number of instances in it has reached the maximum limit, a new security group will be created automatically. |
| io_optimized             | String        |   No        | false          |                              | I/O optimized<br/>• **false**: no I/O Optimized<br/>• **true**: I/O Optimized |
| vswitch_id               | String        |   No        |                |                              | The subnet ID in which to launch the instance (VPC). |
| instance_name            | String        |   No        |                |                              | Display name of the instance, which is a string of 2 to 128 Chinese or English characters. It must begin with an uppercase/lowercase letter or a Chinese character and can contain numerals, “.”, “_“, or “-“. The instance name is displayed on the Alibaba Cloud console. If this parameter is not specified, the default value is InstanceId of the instance. It cannot begin with http:// or https://. |
| description              | String        |   No        |                |                              | Description of the instance, which is a string of 2 to 256 characters. The instance description is displayed on Alibaba Cloud console. If this parameter is not specified, it is null. The default value is null. It cannot begin with http:// or https://.|
| internet_data            | Dictionary    |   No        |                |                              | A hash/dictionaries of InternetData attributes. Refer table [Internet Data Declaration](#internet-data-declaration) |
| host_name                | String        |   No        |                |                              | Host name of the ECS, which is a string of at least two characters. hostname cannot start or end with “.” or “- “. In addition, two or more consecutive “.” or “-“ symbols are not allowed. On Windows, the host name can contain a maximum of 15 characters, which can be a combination of uppercase/lowercase letters, numerals, and “- “. The host name cannot contain dots (“.”) or contain only numeric characters. On other OSs such as Linux, the host name can contain a maximum of 30 characters, which can be segments separated by dots (“.”), where each segment can contain uppercase/lowercase letters, numerals, or “_ “. |
| password                 | String        |   No        |                |                              | Password to an instance is a string of 8 to 30 characters. It must contain uppercase/lowercase letters and numerals, but cannot contain special symbols. |
| system_disk              | Dictionary    |   No        |                |                              | A hash/dictionaries of system disk to the new instance. Refer table [System Disk Declaration](#system-disk-declaration).|
| volumes                  | List          |   No        |                |                              | A list of hash/dictionaries of volumes to add to the new instance. Refer table [Volume Declaration](#volume-declaration).|
| count                    | Integer       |   No        | 1              |                              | The number of instances to launch. |
| allocate_public_ip       | String        |   No        | true           |                              | Whether allocate a public IP for the new instance. |
| bind_eip                 | String        |   No        |                |                              | ID of Elastic IP Address bind to the new instance. |   
| instance_tags            | List          |   No        |                |                              | A list of hash/dictionaries of instance tags, [{tag_key: "value", tag_value: "value"}], tag_key must be not null when tag_value isn't null |
| ids                      | List          |   No        |                |                              | A list of identifier for this instance or set of instances, so that the module will be idempotent with respect to ECS instances. This identifier should not be reused for another call later on. For details, see the description of client token at https://help.aliyun.com/document_detail/25693.html?spm=5176.doc25499.2.7.mrVgE2. |
| instance_charge_type     | String        |   No        | PostPaid       | PrePaid/PostPaid             | Payment methods.<br/>• **PrePaid**: prepayment, that is, monthly/yearly subscription. Users who select the type of payment method must ensure that the credit payment is available for their accounts; otherwise it will return invalid payment method.<br/>• **PostPaid**: post-paid, that is, pay-as-you-go.|
| period                   | Integer       |   No        |                |                              | The time that you have bought the resource, in month. Only valid when InstanceChargeType is set as PrePaid. Value range: 1 to 12 |
| auto_renew               | String        |   No        | false          |                              | Whether automatic renewal is supported. Only valid when InstanceChargeType is set PrePaid. Value range<br/>•	**true**，indicates to automatically renew<br/>• **false**，indicates not to automatically renew |
| auto_renew_period        | Integer       |   No        |                |                              | The duration of the automatic renew the charge of the instance. It is valid when auto_renew is true. Allowed values are 1, 2, 3, 6, 12 

### Internet Data Declaration

| Parameter	               | Type	       | Required    | Default        |   Choice	                 |   Description   |
|----------------------    |---	           |---	         |---	          |---	                         |---              |  
| charge_type              | String        |   No	     | PayByBandwidth | PayByBandwidth PayByTraffic  | Internet charge type, which can be PayByTraffic or PayByBandwidth. Optional values:<br/>• **PayByBandwidth**<br/>• **PayByTraffic** If this parameter is not specified.|
| max_bandwidth_in         | Integer       |   No        | 200            |                              | Maximum incoming bandwidth from the public network, measured in Mbps (Mega bit per second). Value range: [1,200] If this parameter is not specified, API automatically sets it to 200 Mbps.|
| max_bandwidth_out        | Integer       |   No        | 0              |                              | Maximum outgoing bandwidth to the public network, measured in Mbps (Mega bit per second). Value range: PayByBandwidth: [0, 100]. If this parameter is not specified, API automatically sets it to 0 Mbps. PayByTraffic: [1, 100]. If this parameter is not specified, an error is returned.|

### System Disk Declaration

| Parameter	               | Type	       | Required    | Default        |   Choice	                 |   Description   |
|----------------------    |---	           |---	         |---	          |---	                         |---              |  
| disk_category            | String        |   No	     | cloud          | cloud cloud_efficiency cloud_ssd ephemeral_ssd | Category of the system disk Optional values are:<br/>•  **cloud** - basic cloud disk<br/>• **cloud_efficiency** - ultra cloud disk<br/>• **cloud_ssd** - cloud SSD<br/>• **ephemeral_ssd** - ephemeral SSD. Note: For I/O optimized instance type, SSD and ultra cloud disks are supported. For non I/O Optimized instance type, local SSD and basic cloud disks are supported. |
| disk_size                | Integer       |   No	     |                |                              | Size of the system disk, in GB, value range:<br/>• Cloud - 40 ~ 500<br/>• cloud_efficiency - 40 ~ 500<br/>• cloud_ssd - 40 ~ 500<br/>•	ephemeral_ssd - 40 ~ 500 Default value: size=max{40，ImageID}. The value should be equal to or greater than max{40，ImageID}.  |
| disk_name                | String        |   No	     |                |                              | Name of a system disk, which is a string of 2 to 128 Chinese or English characters. It can contain numerals, “_“, or “-“. It must begin with an uppercase/lowercase letter or a Chinese character. If this parameter is not specified, it is null. The default value is null. The disk name is displayed on Alibaba Cloud console. It cannot begin with http:// or https://. |
| disk_description         | String        |   No	     |                |                              | Description of a system disk, which is a string of 2 to 256 characters. The instance description is displayed on the Alibaba Cloud console. If this parameter is not specified, it is null by default. It cannot begin with http:// or https://. |

### Volume Declaration

| Parameter	               | Type	       | Required    | Default        |   Choice	                 |   Description   |
|----------------------    |---	           |---	         |---	          |---	                         |---              |  
| device_size              | Integer       |   No	     |                |                              | Size of the n volume, n starts from 1. In GB, value range:<br/>•	cloud - 5 ~ 2000<br/>• cloud_efficiency - 20 ~ 2048<br/>• cloud_ssd - 20 ~ 2048<br/>• ephemeral_ssd - 5 ~ 800.<br/>The value should be equal to or greater than the specific snapshot.|
| device_category          | String        |   No	     | cloud          | cloud cloud_efficiency cloud_ssd ephemeral_ssd | Category of the volume n <br/>Optional values are: <br/>• **cloud** - basic cloud disk<br/>• **cloud_efficiency** - ultra cloud disk<br/>• **cloud_ssd** - cloud SSD<br/>• **ephemeral_ssd** - ephemeral SSD<br/>|
| snapshot                 | String        |   No	     |                |                              | snapshot |
| device_name              | String        |   No	     |                |                              | Name of a volume, which is a string of 2 to 128 Chinese or English characters. If this parameter is not specified, it is null by default. The volume name must begin with an uppercase/lowercase letter or a Chinese character, and can contain numerals, “_“, or “-“. The volume name is displayed on the Alibaba Cloud console. It cannot begin with http:// or https://.|
| device_description       | String        |   No	     |                |                              | Description of a volume, which is a string of 2 to 256 characters. If this parameter is not specified, it is null by default. The volume description is displayed on the Alibaba Cloud console. It cannot begin with http:// or https://.|
| delete_on_termination    | String        |   No	     | true           |                              | Whether a volume is released with the instance.<br/>• **true** indicates that the volume is released with the instance<br/>•	**false** indicates that the volume is not released with the instance <br/>This parameter is valid only for an independent basic cloud volume, or when Volume.n.Category=cloud. Otherwise, an error is returned.|

## Examples
```yaml
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
``` 

## Notes
> Note:
If `acs_access_key` parameter is not set within the module, the following environment variables can be used `ACS_ACCESS_KEY_ID` or `ACS_ACCESS_KEY` or `ECS_ACCESS_KEY`.

> Note:
If `acs_secret_access_key` parameter is not set within the module, the following environment variables can be used `ACS_SECRET_ACCESS_KEY` or `ACS_SECRET_KEY` or `ECS_SECRET_KEY`.

> Note:
If `region` parameter is not set within the module, the following environment variables can be used `ACS_REGION`, `ACS_DEFAULT_REGION` or `ECS_REGION`.


###### Module Status: stableinterface

###### This is module is supported by: core
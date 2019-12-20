# Ansible-Alicloud Change Log
## 1.16.0 (Unreleased)

## 1.15.0 (21 January, 2020)
- fix inventory bug use ecs role name ([#230](https://github.com/alibaba/ansible-provider/pull/230))
- improve(rds): Add rds policy module ([#221](https://github.com/alibaba/ansible-provider/pull/221))
- improve(rds): Modify rds account module ([#222](https://github.com/alibaba/ansible-provider/pull/222))
- improve(rds): Add rds backup module ([#223](https://github.com/alibaba/ansible-provider/pull/223))
- improve(ecs): add new param unique_suffix ([#228](https://github.com/alibaba/ansible-provider/pull/228))
- improve (rds): modify rds instance and database ([#205](https://github.com/alibaba/ansible-provider/pull/205))
- fix inventory bug ([#217](https://github.com/alibaba/ansible-provider/pull/217))
- improve(slb): Add tags ([#219](https://github.com/alibaba/ansible-provider/pull/219))

## 1.14.0 (11 December, 2019)
- support profile authentication ([#208](https://github.com/alibaba/ansible-provider/pull/208))
- improve(inventory): Support more authentication methods ([#209](https://github.com/alibaba/ansible-provider/pull/209))

## 1.13.0 (3 December, 2019)
- Add new module ali_dns_domain, ali_dns_domain_info and test case([#201](https://github.com/alibaba/ansible-provider/pull/201))
- Add new module ali_dns_group, ali_dns_group_info and test case ([#202](https://github.com/alibaba/ansible-provider/pull/202))
- improve(ecs): change method create_instances to run_instances ([#194](https://github.com/alibaba/ansible-provider/pull/194))

## 1.12.1 (13 November, 2019)
- improve(ecs): improve(ecs): support create spot instance ([#196](https://github.com/alibaba/ansible-provider/pull/196))
- improve(slb): Fix the error of passing parameters and add testcase ([#199](https://github.com/alibaba/ansible-provider/pull/199))

## 1.12.0 (12 November, 2019)

IMPROVEMENTS:
- support modify route entry's name ([#179](https://github.com/alibaba/ansible-provider/pull/179))
- support query instance more than 10 results ([#182](https://github.com/alibaba/ansible-provider/pull/182))
- change facts to info ([#183](https://github.com/alibaba/ansible-provider/pull/183))
- fix ali_eni module bug caused by not passing description ([#188](https://github.com/alibaba/ansible-provider/pull/188))
- resolve warning of the same name ([#186](https://github.com/alibaba/ansible-provider/pull/186))
- add 'try in cloud shell' button into readme ([#182](https://github.com/alibaba/ansible-provider/pull/182))
- add ram_role_name param for ecs ([#190](https://github.com/alibaba/ansible-provider/pull/190))
- support ecs role name ([#191](https://github.com/alibaba/ansible-provider/pull/191))
- support assume role ([#189](https://github.com/alibaba/ansible-provider/pull/189))
- improve(vpc): add tags param ([#192](https://github.com/alibaba/ansible-provider/pull/192))

## 1.11.0 (October 16, 2019)

IMPROVEMENTS:

- improve example alicloud-ecs-vpc ([#175](https://github.com/alibaba/ansible-provider/pull/175))
- improve code to python3 （[#176](https://github.com/alibaba/ansible-provider/pull/176)）
- Add ali_route_entry test case （[#177](https://github.com/alibaba/ansible-provider/pull/177)）

BUG FIXES:

- Fix create_instance's max_bandwidth_in error ([#177](https://github.com/alibaba/ansible-provider/pull/177)）

## 1.10.0 (11 July, 2019)

IMPROVEMENTS:

- Publish release 1.10.0 ([#172](https://github.com/alibaba/ansible-provider/pull/172))
- Sync alicloud instance modules with the latest ansible ([#171](https://github.com/alibaba/ansible-provider/pull/171))
- Match the latest method describe_instances in footmark 1.12.0 ([#171](https://github.com/alibaba/ansible-provider/pull/171))
- Add creation_time attribute in ali_image_facts results ([#164](https://github.com/alibaba/ansible-provider/pull/164))

BUG FIXES:

- Fix incorrect destination address when hostname_variable equals with destination_address ([#170](https://github.com/alibaba/ansible-provider/pull/170))
- Fix grouping dynamic inventory on security group bug ([#169](https://github.com/alibaba/ansible-provider/pull/169))
- Default to describe all instances in all regions ([#158](https://github.com/alibaba/ansible-provider/pull/158))
- Fix ecs_instance_filters last page describe bug ([#157](https://github.com/alibaba/ansible-provider/pull/157))
- Fix ecs_instance_filters's page_size bug ([#156](https://github.com/alibaba/ansible-provider/pull/156))

## 1.9.0 (4 January, 2019)

FEATURES:

- **New Module:** `ali_eip_facts` ([#144](https://github.com/alibaba/ansible-provider/pull/144))

IMPROVEMENTS:

- Improve test cases ([#154](https://github.com/alibaba/ansible-provider/pull/154))
- Improve inventory alicloud.py meta and use public_ip_address instead eip_address ([#152](https://github.com/alibaba/ansible-provider/pull/152))
- Improve module ali_vpc and ali_security_group multi_ok ([#149](https://github.com/alibaba/ansible-provider/pull/149))
- Improve module ali_slb_vsg and ali_slb_vsg_facts ([#148](https://github.com/alibaba/ansible-provider/pull/148))
- Improve module ali_slb_lb and ali_slb_lb_facts ([#147](https://github.com/alibaba/ansible-provider/pull/147))
- Improve ecs instance and eni docs ([#146](https://github.com/alibaba/ansible-provider/pull/146))
- Improve module ali_eip and add its testcase ([#145](https://github.com/alibaba/ansible-provider/pull/145))
- Improve dynamic inventory by setting page_size 100 ([#142](https://github.com/alibaba/ansible-provider/pull/142))
- Improve ali_security_group and make it idempotence ([#137](https://github.com/alibaba/ansible-provider/pull/137))
- Improve ali_vswitch and make it idempotence ([#136](https://github.com/alibaba/ansible-provider/pull/136))
- Improve ali_vpc and make it idempotence ([#135](https://github.com/alibaba/ansible-provider/pull/135))

BUG FIXES:

- Fix regions=all not working bug in dynamic inventory ([#141](https://github.com/alibaba/ansible-provider/pull/141))

## 1.8.0 (12 November, 2018)

IMPROVEMENTS:

- Improve examples/alicloud-ecs-vpc ([#133](https://github.com/alibaba/ansible-provider/pull/133))
- Improve filters ([#132](https://github.com/alibaba/ansible-provider/pull/132))
- Add tags for ali_eni ([#131](https://github.com/alibaba/ansible-provider/pull/131))
- Improve module ali_eni and ali_eni_facts ([#130](https://github.com/alibaba/ansible-provider/pull/130))
- Add test cases for the ali_eni and ali_eni_facts([#130](https://github.com/alibaba/ansible-provider/pull/130))
- Add name_prefix and tags for the ali_eni_facts ([#130](https://github.com/alibaba/ansible-provider/pull/130))
- Improve module ali_eni and ali_eni_facts ([#130](https://github.com/alibaba/ansible-provider/pull/130))
- Improve dynamic inventory grammar ([#128](https://github.com/alibaba/ansible-provider/pull/128))

BUG FIXES:

- Fix ali_security_group_facts's tags invalid ([#130](https://github.com/alibaba/ansible-provider/pull/130))

## 1.7.0 (2 November, 2018)

IMPROVEMENTS:

- Add tags for ali_security_group ([#127](https://github.com/alibaba/ansible-provider/pull/127))
- Add name_prefix for ali_security_group_facts ([#127](https://github.com/alibaba/ansible-provider/pull/127))
- Add name_prefix and cidr_prefix for ali_vpc_facts ([#126](https://github.com/alibaba/ansible-provider/pull/126))
- Add name_prefix and filters for ali_instance_facts ([#125](https://github.com/alibaba/ansible-provider/pull/125))
- Improve alicloud inventory based on footmark 1.6.3+ ([#124](https://github.com/alibaba/ansible-provider/pull/124))
- Improve ali_security_group and support purge_rules and purge_rules_egress ([#123](https://github.com/alibaba/ansible-provider/pull/123))

## 1.6.0 (October 30, 2018)

IMPROVEMENTS:

- Add alias for security_groups and availability_zone ([#122](https://github.com/alibaba/ansible-provider/pull/122))
- Improve ali_vpc, ali_vpc_facts, ali_vswitch and ali_vswitch_facts using footmark 1.6.0 ([#121](https://github.com/alibaba/ansible-provider/pull/121))
- Add ali_vpc and ali_vswitch test case ([#121](https://github.com/alibaba/ansible-provider/pull/121))
- Add purge_tags for ali_instance ([#119](https://github.com/alibaba/ansible-provider/pull/119))
- Improve ali_instance, ali_instance_facts, ali_security_group and ali_ali_security_group_facts using footmark 1.6.0 ([#119](https://github.com/alibaba/ansible-provider/pull/119))
- Add ali_instance test case ([#119](https://github.com/alibaba/ansible-provider/pull/119))
- Add destroy.yml for examples/alicloud_ecs_vpc ([#117](https://github.com/alibaba/ansible-provider/pull/117))
- Improve roles test cases ([#116](https://github.com/alibaba/ansible-provider/pull/116))
- Improve example/alicloud-ecs-vpc ([#114](https://github.com/alibaba/ansible-provider/pull/114), [#115](https://github.com/alibaba/ansible-provider/pull/115))
- Change nested_groups default to False ([#113](https://github.com/alibaba/ansible-provider/pull/113git ))
- Add to_safe method for dynamic inventory ([#112](https://github.com/alibaba/ansible-provider/pull/112))

BUG FIXED:

- Fix ali_instance_facts filter is None bug ([#120](https://github.com/alibaba/ansible-provider/pull/120))
- Correct module docs ([#103](https://github.com/alibaba/ansible-provider/pull/103))
- Fix nested_groups bug ([#111](https://github.com/alibaba/ansible-provider/pull/111))


## 1.5.0 (July 4, 2018)

IMPROVEMENTS:

- **New Module:** ali_eni ([#102](https://github.com/alibaba/ansible-provider/pull/102))
- **New Module:** ali_eni_facts ([#102](https://github.com/alibaba/ansible-provider/pull/102))
- Rename all module prefix and use 'ali' instead ([#102](https://github.com/alibaba/ansible-provider/pull/102))
- Improve README ([#88](https://github.com/alibaba/ansible-provider/pull/88))

IMPROVEMENTS:

- Improve README ([#88](https://github.com/alibaba/ansible-provider/pull/88))

## 1.3.2 (January 23, 2018)

BUG FIXED:

    * fix creating multiple security group error from [issue 82](https://github.com/alibaba/ansible-provider/issues/82) ([#82](https://github.com/alibaba/ansible-provider/pull/82))

## 1.3.0 (January 23, 2018)

Pip package is unavailable.

## 1.3.0 (January 10, 2018)

IMPROVEMENTS:

  * **New Module:** alicloud_ess_rule ([#81](https://github.com/alibaba/ansible-provider/pull/81))
  * **New Module:** alicloud_ess_task ([#81](https://github.com/alibaba/ansible-provider/pull/81))
  * Remove all ECS instances in the specified ESS Group ([#81](https://github.com/alibaba/ansible-provider/pull/81))
  * Modify alicloud_ess_instance to remove all instances in the ESS Group ([#81](https://github.com/alibaba/ansible-provider/pull/81))


## 1.2.0 (January 8, 2018)

IMPROVEMENTS:

  * **New Module:** alicloud_ess_group ([#79](https://github.com/alibaba/ansible-provider/pull/79))
  * **New Module:** alicloud_ess_configuration ([#79](https://github.com/alibaba/ansible-provider/pull/79))
  * **New Module:** alicloud_ess_instance ([#79](https://github.com/alibaba/ansible-provider/pull/79))
  * Update module 'alicloud_slb_listener' examples spelling error: ([#80](https://github.com/alibaba/ansible-provider/pull/80))


## 1.1.3 (December 20, 2017)

IMPROVEMENTS:

 * alicloud_slb_lb: remove status and add start/stop slb instance ([#78](https://github.com/alibaba/ansible-provider/pull/78))

BUG FIXED:

 * alicloud_slb_listener: fix listener not found ([#78](https://github.com/alibaba/ansible-provider/pull/78))


## 1.1.1 (November 13, 2017)

NEW RESOURCE MODULES:

    * alicloud_eip: new module for EIP ([#76](https://github.com/alibaba/ansible-provider/pull/76))

## 1.0.12 (November 6, 2017)

IMPROVEMENTS:

  * alicloud_instance: add key pair and userdata ([#69](https://github.com/alibaba/ansible-provider/pull/69))


## 1.0.12 (November 6, 2017)

IMPROVEMENTS:

  * alicloud_instance: add key pair and userdata ([#69](https://github.com/alibaba/ansible-provider/pull/69))


## 1.0.12 (November 6, 2017)

IMPROVEMENTS:

  * alicloud_instance: add key pair and userdata ([#69](https://github.com/alibaba/ansible-provider/pull/69))


## 1.0.11 (November 2, 2017)

IMPROVEMENTS:

  * add client token for disk, group, vpc, vswitch, slb and rds ([#67](https://github.com/alibaba/ansible-provider/pull/67))
  * modify footmark version for all module ([#67](https://github.com/alibaba/ansible-provider/pull/67))


## 1.0.10 (November 2, 2017)

IMPROVEMENTS:

  * alicloud/alicloud_instance.py: add client_token and improve code according to Ansible official ([#67](https://github.com/alibaba/ansible-provider/pull/67))


## 1.0.9(October 24, 2016)

  * **New Module:** `alicloud_instance`
  * **New Module:** `alicloud_security_group`
  * **New Module:** `alicloud_slb`
  * **New Module:** `alicloud_vpc`
  * **New Module:** `alicloud_vswitch`
  * **New Module:** `alicloud_route_entry`
  * **New Module:** `alicloud_bucket`
  * **New Module:** `alicloud_bucket_object`
  * **New Module:** `alicloud_instance_facts`
  * **New Module:** `alicloud_instance_type_facts`

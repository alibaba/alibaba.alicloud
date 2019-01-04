# Ansible-Alicloud Change Log
## 1.10.0 (Unreleased)
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

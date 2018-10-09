# Ansible-Alicloud Change Log

## 1.5.1 (Unreleased)

IMPROVEMENTS:

- Add to_safe method for dynamic inventory ([#112](https://github.com/alibaba/ansible-provider/pull/112))

BUG FIXED:

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

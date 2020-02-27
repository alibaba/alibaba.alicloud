#!/usr/bin/python
# Copyright (c) 2017-present Alibaba Group Holding Limited. He Guimin <heguimin36@163.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
#  This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see http://www.gnu.org/licenses/.


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ali_market_product_info
version_added: "2.9"
short_description: Gather info on Market product of Alibaba Cloud.
description:
     - Gather info on Market product of Alibaba Cloud.
options:
  name_prefix:
    description:
      - Use a product name prefix to filter products.
  search_term:
    description:
      - Search term in this query.
  sort:
    description:
      - This field determines how to sort the filtered results.
    choices: ['user_count-desc', 'created_on-desc', 'price-desc', 'score-desc']
  category_id:
    description:
      - The Category ID of products. For more information. see more (https://help.aliyun.com/document_detail/89834.htm).
  product_type:
    description:
      - The type of products.
    choices: ["APP", "SERVICE", "MIRROR", "DOWNLOAD", "API_SERVICE"]
  suggested_price:
    description:
      - The suggested price of the product.
  supplier_id:
    description:
      - The supplier id of the product.
  supplier_name_keyword:
    description:
      - The supplier name keyword of the product.
  ids:
    description:
      - A list of product code.

author:
    - "He Guimin (@xiaozhu36)"
requirements:
    - "python >= 3.6"
    - "footmark >= 1.18.0"
extends_documentation_fragment:
    - alicloud
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the Alibaba Cloud Guide for details.

- name: Search products
  ali_market_product_info:
    search_term: 'YourSearchTerm'
    product_type: MIRROR
    category_id: '53616009'
    suggested_price: 0

'''

RETURN = '''
products:
    description: A list of product.
    returned: always
    type: complex
    contains:
        code:
            description: The code of the product.
            returned: always
            type: string
            sample: cmjj016644
        name:
            description: The name of the product.
            returned: always
            type: string
            sample: WordPress博客环境(Centos6.8 64位 )
        score:
            description: The score of the product.
            returned: always
            type: float
            sample: 4.7
        short_description:
            description: The short description of the product.
            returned: always
            type: string
            sample: "集成Nginx1.13、PHP5.6、PHPMYADMIN4.6.6、MySQL 5.6.34、WordPress4.7.3"            
        type:
            description: The type of the product.
            returned: always
            type: string
            sample: MIRROR
        images:
            description: The type of the product.
            returned: always
            type: list
            contains:
                - display_name:
                      description: The display name of image.
                      returned: always
                      type: string
                      sample: 华北 1_V1.1
                - type:
                      description: The type of the image.
                      returned: always
                      type: string
                      sample: single_string
                - value:
                      description: The id of image.
                      returned: always
                      type: string
                      sample: m-2ze0ua7jvif73kxxxxx
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.alicloud_ecs import ecs_argument_spec, market_connect

HAS_FOOTMARK = False

try:
    from footmark.exception import MARKETResponseError
    HAS_FOOTMARK = True
except ImportError:
    HAS_FOOTMARK = False


def main():
    argument_spec = ecs_argument_spec()
    argument_spec.update(dict(
        name_prefix=dict(typr='str'),
        search_term=dict(type='str'),
        sort=dict(type='str', choices=['user_count-desc', 'created_on-desc', 'price-desc', 'score-desc']),
        category_id=dict(type='str'),
        product_type=dict(type='str', choices=["APP", "SERVICE", "MIRROR", "DOWNLOAD", "API_SERVICE"]),
        suggested_price=dict(type='float'),
        supplier_id=dict(type='str'),
        supplier_name_keyword=dict(type='str'),
        ids=dict(typr='list')
    )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if HAS_FOOTMARK is False:
        module.fail_json(msg="Package 'footmark' required for this module.")

    Filters = []
    if module.params['sort']:
        Filters.append({'Key': 'sort', 'Value': module.params['sort']})
    if module.params['product_type']:
        Filters.append({'Key': 'productType', 'Value': module.params['product_type']})
    if module.params['category_id']:
        Filters.append({'Key': 'categoryId', 'Value': module.params['category_id']})

    if Filters:
        module.params['Filters'] = Filters

    name_prefix = module.params['name_prefix']
    suggested_price = module.params['suggested_price']
    supplier_id = module.params['supplier_id']
    supplier_name_keyword = module.params['supplier_name_keyword']
    ids = module.params['ids']

    products = []
    try:
        for product in market_connect(module).describe_products(**module.params):
            if name_prefix and not product.name.startswith(name_prefix):
                continue
            if supplier_id and str(product.supplier_id) != supplier_id:
                continue
            if supplier_name_keyword and product.supplier_name_keyword.find(supplier_name_keyword) == -1:
                continue
            if (suggested_price or suggested_price == 0) and not product.suggested_price.startswith(str(suggested_price).replace('.0', '') if str(suggested_price).endswith('.0') else str(suggested_price)):
                continue
            if ids and product.code not in ids:
                continue
            products.append(product.get().read())
        module.exit_json(changed=False, products=products)
    except Exception as e:
        module.fail_json(msg=str("Unable to get products, error:{0}".format(e)))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# Always prefer setuptools over distutils
from codecs import open
from os import path

try:
    from setuptools import setup, find_packages

    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup

    extra = {}

NAME = "ansible_alicloud"
DESCRIPTION = "Ansible provider for Alicloud."
AUTHOR = "xiaozhu"
AUTHOR_EMAIL = "heguimin36@163.com"
URL = "https://github.com/alibaba/ansible-provider/tree/master/lib/ansible"

VERSION = "1.0.1.dev15"

setup(
    name="ansible_alicloud",

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version=PROVIDER_VERSION,
    version=VERSION,
    description=DESCRIPTION,

    url=URL,

    # Author details
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    packages=['ansible.module_utils', 'ansible.modules', 'ansible.modules.cloud', 'ansible.modules.cloud.alicloud',
              'ansible.utils', 'ansible.utils.module_docs_fragments'],
    include_package_data=True,
    install_requires=['ansible', 'footmark>=1.1.6', 'ansible_alicloud_module_utils', 'importlib']
)

########################################################################
# # !!!!!!!!!!!!!! NOTE:
# # The following code is to package ansible_alicloud_module_utils. You must annotated above code before package it.

NAME_UTILS = "ansible_alicloud_module_utils"
DESCRIPTION_UTILS = "The dependence of Ansible Provider Alicloud modules."

VERSION_UTILS = '1.0.3'

URL_UTILS = 'https://github.com/alibaba/ansible-provider/tree/master/lib/ansible/module_utils'

setup(
    name=NAME_UTILS,

    version=VERSION_UTILS,
    description=DESCRIPTION_UTILS,

    # Author details
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    url=URL_UTILS,

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    packages=['ansible.module_utils'],
    include_package_data=True,
    install_requires=['ansible']
)

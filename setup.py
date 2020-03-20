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

VERSION = "1.18.0"

setup(
    name=NAME,

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
        # that you indicate whether you support Python 3.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    include_package_data=True,
    install_requires=['ansible', 'footmark>=1.19.0', 'ansible_alicloud_module_utils>=1.4.0']
)

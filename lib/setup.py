#!/usr/bin/env python
# Always prefer setuptools over distutils

try:
    from setuptools import setup

    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup

    extra = {}

NAME = "ansible_alicloud_module_utils"
DESCRIPTION = "The dependence of Ansible Provider Alicloud modules."
AUTHOR = "xiaozhu"
AUTHOR_EMAIL = "heguimin36@163.com"

VERSION = '1.5.0'

setup(
    name=NAME,

    version=VERSION,
    description=DESCRIPTION,

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
        'Programming Language :: Python :: 3.6',
    ],

    packages=['ansible.module_utils'],
    include_package_data=True,
    install_requires=['ansible', 'footmark>=1.20.0']
)

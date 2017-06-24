#!/usr/bin/env python3

from setuptools import setup

package = {
    "name": 'occquse',
    "packages": ['occquse'],
    "include_package_data": True,
    "install_requires": ['flask','toml']
}

setup(**package)



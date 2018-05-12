#!/usr/bin/env python3

from setuptools import setup

package = {
    "name": 'survey_display',
    "packages": ['survey_display'],
    "include_package_data": True,
    "install_requires": ['flask','toml']
}

setup(**package)


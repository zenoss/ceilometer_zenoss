##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = [
    'ceilometer',
    'kombu',
    'eventlet'
]


setup(
    name='ceilometer_zenoss',
    packages=find_packages(),
    package_data={
        '': ['*.yaml'],
    },
    entry_points={
        'ceilometer.dispatcher': 'zenoss = ceilometer_zenoss.dispatcher.zenoss:ZenossDispatcher'
    },

    version='1.0.2',
    description="Ceilometer dispatcher plugin to ship data to Zenoss.",
    long_description=read('README.rst'),

    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: OpenStack',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Monitoring',
        'Natural Language :: English',
    ],

    keywords="openstack ceilometer zenoss",
    author='Zenoss, Inc.',
    author_email='support@zenoss.com',
    url='http://github.com/zenoss/ceilometer_zenoss',
    license="Apache License, Version 2.0",

    requires=requires,
    install_requires=requires,
    zip_safe=False
)

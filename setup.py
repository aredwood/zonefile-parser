#!/usr/bin/env python
"""
DNS Zone File
==============

"""

from setuptools import setup, find_packages

setup(
    name='zone-file-parser',
    version='0.1.0',
    url='https://github.com/aredwood/zone-file-parser',
    license='MIT',
    author='Alex Redwood',
    author_email='hello@alexredwood.com',
    maintainer='Alex Redwood',
    maintainer_email='hello@alexredwood.com',
    description="library for parsing dns zone files",
    keywords='parse dns zone file',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
    ],
    classifiers=[

    ]
)

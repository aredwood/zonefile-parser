#!/usr/bin/env python
"""
DNS Zone File
==============

"""

from setuptools import setup, find_packages


version = "0.1.9"


setup(
    name='zonefile_parser',
    version=version,
    url='https://github.com/aredwood/zone-file-parser',
    license='MIT',
    author='Alex Redwood',
    download_url=f"https://github.com/aredwood/zone-file-parser/archive/{version}.tar.gz",
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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)

#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='cortex4py',
    version='2.1.0',
    description='Python API client for Cortex.',
    long_description=read_md('README.md'),
    author='TheHive-Project',
    author_email='support@thehive-project.org',
    maintainer='TheHive-Project',
    url='https://github.com/Thehive-Project/Cortex4py',
    license='AGPL-V3',
    packages=['cortex4py', 'cortex4py.models', 'cortex4py.controllers'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    include_package_data=True,
    install_requires=['typing', 'requests', 'python-magic']
)

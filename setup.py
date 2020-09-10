#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

config = {
    'name': 'rwuser',
    'version': '0.0.3',
    'author': 'Florian Ludwig',
    'description': 'rueckenwind helpers for user management',
    'long_description': readme,
    'author_email': 'f.ludwig@greyrook.com',
    'url': 'https://github.com/FlorianLudwig/rwuser',
    
    'install_requires': ['pytest', 'perm', 'fpt'],
    'packages': ['rwuser'],
    'entry_points': {
        'console_scripts': [
            'rwuser = rwuser.cli:main',
        ],
    },
    'license=': "Apache Software License 2.0",
    'classifiers': [
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
}

setup(**config)

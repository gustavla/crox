#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

from setuptools import setup
import os

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
]

args = dict(
    name='crox',
    version='0.1.0',
    url="https://github.com/gustavla/crox",
    description="Light-weight general-purpose macro expander",
    maintainer='Gustav Larsson',
    maintainer_email='gustav.m.larsson@gmail.com',
    scripts=['scripts/crox'],
    packages=[
        'crox',
    ],
    license='BSD',
    classifiers=CLASSIFIERS,
)

setup(**args)

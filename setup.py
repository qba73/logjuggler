#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='logjuggler',
    version='0.1.0',
    description='A simple log parser.',
    long_description=readme + '\n\n' + history,
    author='Jakub Jarosz',
    author_email='jakub.s.jarosz@gmail.com',
    url='https://github.com/qba73/logjuggler',
    packages=[
        'logjuggler',
    ],
    package_dir={'logjuggler': 'logjuggler'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='logjuggler',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers, Testers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ],
)

#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='orderprocessor',
    version='1.1',
    description='Dispatches Linnworks orders',
    author='Luke Shiner',
    install_requires=['termcolor', 'colorama'],
    packages=find_packages(),
    )

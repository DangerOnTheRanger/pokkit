#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

setup(
    name='pokkit',
    version='0.1',
    description='',
    author='',
    url='https://github.com/DangerOnTheRanger/',
    packages=find_namespace_packages(),
    install_requires=['PyQt5', 'fusepy', 'requests', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'pokkit-client = pokkit.client.__main__:main',
        ],
    },
)

#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_namespace_packages

setup(
    name='Pokkit Server',
    version='0.1',
    description='',
    author='',
    url='https://github.com/DangerOnTheRanger/',
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'pokkit-server = pokkit.server.__main__:main'
        ],
    },
)

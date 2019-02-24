#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

<<<<<<< HEAD
setup(name='pokkit',
      version='0.1',
      description='',
      author='',
      url='https://github.com/DangerOnTheRanger/',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': [
          'pokkit = pokkit.client.__main__:main'
      ]},
      install_requires=[
          'fuse-python'
          ],
     )
=======
setup(
    name='pokkit',
    version='0.1',
    description='',
    author='',
    url='https://github.com/DangerOnTheRanger/',
    packages=find_namespace_packages(),
    install_requires=['PyQt5', 'fuse-python'],
    entry_points={
        'console_scripts': [
            'pokkit = pokkit.client.__main__:main',
        ],
    },
)
>>>>>>> 899e9ffff3a0458e39f833734c4dce9fb2b6b553

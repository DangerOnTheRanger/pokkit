#!/usr/bin/env python3

from distutils.core import setup


setup(name='Pokkit',
      version='0.1',
      description='',
      author='',
      url='https://github.com/DangerOnTheRanger/',
      package_dir={'pokkit.client': 'lib'},
      entry_points={'console_scripts': [
          'pokkit = pokkit.client.__main__:main'
      ]},
     )

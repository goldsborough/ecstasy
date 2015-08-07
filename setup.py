# -*- coding: utf-8 -*-

"""
setup.py script for setuptools.
"""

import os
import re

from codecs import open

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

version = ''
with open('requests/__init__.py', 'r') as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
						f.read(), re.MULTILINE).group(1)

with open('README.rst', encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='ecstasy',

	version='1.0',

	description='A command-line beautification tool.',
	long_description=long_description,

	url='https://github.com/goldsborough/ecstasy',

	author='Peter Goldsborough',
	author_email='petergoldsborough@hotmail.com',

	license='MIT',

	classifiers=[
		'Development Status :: 4 - Beta',

		'Intended Audience :: Developers',
		'Topic :: Software Development',

		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	],

	keywords='command-line tools formatting styling',

	packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)

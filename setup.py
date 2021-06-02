"""A setuptools based setup module for Remarker"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requires = [
    'click',
    'jinja2',
    'pyyaml',
]

lint_requires =  ['flake8']

typecheck_requires =  ['mypy']

tests_require =  [
    'pytest',
    'pytest-runner',
    'pytest-cov',
]

setup(
    name='Remarker',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A command line tool to generate Remark.js presentations from markdown files.",
    long_description=readme + '\n\n' + history,
    author="Dave Forgac",
    author_email='tylerdave@tylerdave.com',
    url='https://github.com/tylerdave/remarker',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts':[
            'remarker=remarker.cli:remarker',
            ],
        },
    include_package_data=True,
    package_data = {
        'remarker': ['templates/*'],
        },
    python_requires='>=3.7',
    install_requires=requires,
    extras_require={
        'lint': lint_requires,
        'typecheck': typecheck_requires,
        'tests': tests_require,
    },
    license="MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
)

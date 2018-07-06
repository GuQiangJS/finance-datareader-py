#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import versioneer

NAME = 'finance-datareader-py'


def readme():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=readme(),
    long_description=readme(),
    license='Apache License 2.0',
    author='GuQiangJS',
    author_email='guqiangjs@gmail.com',
    url='https://github.com/GuQiangJS/finance-datareader-py.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
    keywords='data',
    install_requires=['pandas', 'pandas-datareader', 'numpy', 'beautifulsoup4'],
    packages=find_packages(),
    zip_safe=False,
    exclude_package_data={'': ['test_*.py']}
)

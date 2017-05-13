#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession
import os


def read_requirements():
    '''parses requirements from requirements.txt'''
    __location__ = os.path.dirname(os.path.realpath(__file__))
    reqs_path = os.path.join(__location__, 'requirements.txt')
    install_reqs = parse_requirements(reqs_path, session=PipSession())
    reqs = [str(ir.req) for ir in install_reqs]
    return reqs

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = read_requirements()

test_requirements = requirements

setup(
    name='fifthdown',
    version='0.1.0',
    description="Data behind the blocking and tackling",
    long_description=readme,
    author="Zack White",
    author_email='zackwhiteal@gmail.com',
    url='https://github.com/zackwhiteit/fifthdown',
    packages=['fifthdown'],
    entry_points={
        'console_scripts': [
            'fifthdown=fifthdown.fifthdown:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='fifthdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

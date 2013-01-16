# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='whatthepatch',
    version='0.0.2',
    description='A patch parsing library',
    long_description=readme,
    author='Christopher S. Corley',
    author_email='cscorley@ua.edu',
    url='https://github.com/cscorley/whatthepatch',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    keywords = [],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Processing",
        ],
)


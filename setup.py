# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as f:
    readme = f.read()

setup(
    name='whatthepatch',
    version='0.0.6',
    author='Christopher S. Corley',
    author_email='cscorley@crimson.ua.edu',
    description='A patch parsing and application library.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/cscorley/whatthepatch',
    license='MIT',
    packages=['whatthepatch'],
    include_package_data=True,
    keywords=[
        "patch",
        "diff",
        "parser",
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Processing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

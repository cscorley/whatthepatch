# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.rst") as f:
    readme = f.read()

setup(
    name="whatthepatch",
    version="1.0.1",
    author="Christopher S. Corley",
    author_email="cscorley@gmail.com",
    description="A patch parsing and application library.",
    long_description=readme,
    url="https://github.com/cscorley/whatthepatch",
    license="MIT",
    packages=["whatthepatch"],
    include_package_data=True,
    keywords=["patch", "diff", "parser"],
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Processing",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)

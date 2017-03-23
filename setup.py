#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="pyepayco",
    version="1.0.0",
    author="ePayco Development Team",
    author_email="desarrollo@epayco.co",
    packages=['pyepayco'],
    url='https://epayco.co/',
    download_url="https://github.com/epayco/epayco-python",
    license="MIT",
    description="Python library for ePayco Payment API",
    long_description="Basic python library to interact with ePayco Payment API",
    install_requires=[
        "requests >= 2.4.3",
        "pycrypto >= 2.3"
    ],
)
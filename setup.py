#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="epaycosdk",
    version="3.0.1",
    author="ePayco Development Team",
    author_email="ricardo.saldarriaga@epayco.co",
    packages=['epaycosdk'],
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
#!/usr/bin/env python3

from setuptools  import setup, find_packages
import platform

setup(
    name="epaycosdk",
    version="3.1.2",
    include_package_data=True,
    author="ePayco Development Team",
    author_email="ricardo.saldarriaga@epayco.co",
    packages=find_packages(),
    url='https://epayco.co/',
    download_url="https://github.com/epayco/epayco-python",
    license="MIT",
    description="Python library for ePayco Payment API",
    long_description="Basic python library to interact with ePayco Payment API",
    install_requires=[
        "requests >= 2.4.3",
        "pycryptodome >= 2.6.1" if platform.system() == "Windows" else "pycrypto >= 2.6.1",
        "python-dotenv >= 0.19.2"
    ],
)
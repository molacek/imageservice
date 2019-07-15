#!/usr/bin/env python

from setuptools import setup

setup(
    name="imageservice",
    version="0.0.2",
    packages=setuptools.find_packages(),
    scripts=[
        "imageservice/bin/scan",
        "imageservice/bin/image_download",
        "imageservice/bin/rip_post",
    ]
)

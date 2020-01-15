#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="imageservice",
    version="0.0.19",
    packages=setuptools.find_packages(),
    install_requires=["requests", "bs4"],
    scripts=[
        "imageservice/bin/image_download",
        "imageservice/bin/rip_post",
    ],
    test_suite='nose.collector',
    test_require=['nose']
)

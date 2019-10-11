#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="imageservice",
    version="0.0.5",
    packages=setuptools.find_packages(),
    scripts=[
        "imageservice/bin/scan",
        "imageservice/bin/image_download",
        "imageservice/bin/rip_post",
    ],
    test_suite='nose.collector',
    test_require=['nose']
)

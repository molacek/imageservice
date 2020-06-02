#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="imageservice",
    version="0.0.23",
    packages=setuptools.find_packages(),
    install_requires=["requests", "bs4", "xdg"],
    test_suite='nose.collector',
    test_require=['nose']
)

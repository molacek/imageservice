#!/usr/bin/env python

import requests
import re
from bs4 import BeautifulSoup


def get_image_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image = soup.find('img', {'id': 'image'})
    if not image:
        return(False, "Unable to find image on {0:s}".format(url))

    m = re.match("[0-9]*_(.*)", image["alt"])
    if not m:
        return(
            False,
            "Unable to extract filename from {0:s}".format(image["alt"])
        )

    return(True, (image["src"], m.group(1)))

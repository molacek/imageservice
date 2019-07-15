#!/usr/bin/env python

import requests
import sys
from bs4 import BeautifulSoup

def get_image_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image_elements = soup.find_all("div", attrs={"class": "main-image-wrapper"})
    image_element = image_elements[0]
    url = "https:{0:s}".format(image_element["data-src"])
    file_name = image_element["data-filename"]
    return(True, (url, file_name))

#!/usr/bin/env python

import requests
import sys
from bs4 import BeautifulSoup

def get_image_url(url):
    payload = {"imgContinue": "Continue to image ..."}
    r = requests.post(url, data=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    image_elements = soup.find_all("img", attrs={"class": "centred"})
    image_element = image_elements[0]
    url = image_element["src"]
    file_name = image_element["alt"]
    return(True, (url, file_name))

#!/usr/bin/env python

import requests
import sys
from bs4 import BeautifulSoup

def get_image_url(url):
    payload = {"imgContinue": "Continue to image ..."}
    r = requests.post(url, data=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    meta_elements = soup.find_all("meta", attrs={"property": "og:image"})
    meta_element = meta_elements[0]
    url = meta_element["content"]
    file_name = url.split('/')[-1]
    return(True, (url, file_name))

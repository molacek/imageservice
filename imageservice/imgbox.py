#!/usr/bin/env python

import requests
import sys
from bs4 import BeautifulSoup

def get_image_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    meta_elements = soup.find_all("meta", attrs={"property": "og:image"})
    meta_element = meta_elements[0]
    url = meta_element["content"]

    image_container = soup.find("img", {"id": "img"})
    file_name = image_container["title"]

    return(True, (url, file_name))

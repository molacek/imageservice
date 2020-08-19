#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

from . import httpclient


class Imagebam:
    def __init__(self, username=None, password=None, proxy=None):
        self.username = username
        self.password = password
        self.status = None
        self.error = None
        self.logged_in = False
        self.http = httpclient.HttpClient(proxy)
        self.proxy = proxy
        self.thumbnail = None
        self.image = None

    def get_image_url(self, url):
        if url.startswith("https://"):
            url = "http://{0:s}".format(url[8:])
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        meta_elements = soup.find_all("meta", attrs={"property": "og:image"})
        meta_element = meta_elements[0]
        url = meta_element["content"]
        file_name = url.split('/')[-1]
        return(True, (url, file_name))

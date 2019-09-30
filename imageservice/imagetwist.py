import hashlib
import requests
import time
import random
import string
import os
from bs4 import BeautifulSoup
from . import utils


class Imagetwist:

    def __init__(self, username, password, proxies=None):
        self.username = username
        self.password = password
        self.logged_in = False
        self.session = requests.Session()
        self.user_agent = ("Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                           "51.0.2683.0 Safari/537.36")
        self.headers = {
            "user-agent": self.user_agent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/webp,*/*;q=0.8",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1"
        }

        if proxies:
            self.session.proxies.update(proxies)

    def _login(self):

        r = self.session.post(
            "https://imagetwist.com/",
            data={
               "op": "login",
               "redirect": "",
               "login": self.username,
               "password": self.password,
               "submit_btn": "Login"
            }
        )

        bs = BeautifulSoup(r.text, 'html.parser')
        self.sess_id = bs.find('input', {'name': 'sess_id'})["value"]
        self.action = bs.find('form', {'name': 'url'})["action"]

    def upload(self, filename):
        if not self.logged_in:
            self._login()

        # Verify image integrity
        image_integrity_result = utils.verify_integrity(filename)
        if image_integrity_result is not True:
            return(image_integrity_result)

        upload_id = "".join(random.choice(string.digits) for _ in range(12))
        upload_url = "{0:s}{1:s}&js_on=0&utype=reg&" \
            "upload_type=file".format(self.action, upload_id)

        upload_filename = os.path.basename(filename)
        upload_file = {
            "file_0": (
                upload_filename,
                utils.image_buffer(filename, filesize=6000000),
                "image/jpeg"
            ),
            "file_1": (
                "",
                "",
                "application/octet-stream"
            )
        }

        upload_data = {
            "upload_type": "file",
            "sess_id": self.sess_id,
            "thumb_size": "350x350",
            "per_row": "1",
            "sdomain": "imagetwist.com",
            "fld_id": "0",
            "tos": "1",
            "submit_btn": "Upload"
        }

        r = self.session.post(
            upload_url,
            headers=self.headers,
            files=upload_file,
            data=upload_data
        )

        bs = BeautifulSoup(r.text, 'html.parser')
        all_divs = bs.find_all('div')
        n = 0
        for div in all_divs:
            if div.text == 'Preview:':
                thumb = all_divs[n+1].find('img')["src"]
                img = all_divs[n+1].find('a')["href"]
                return(thumb, img)
            n += 1

        return(False)


def validate(thumb_url, sess):

    while True:
        try:
            r = sess.get(thumb_url)
        except requests.exceptions.ConnectionError:
            print("Error connecting to {0:s}".format(thumb_url))
            time.sleep(10)
            continue
        break

    if r.status_code == 404:
        return "not_found"

    if "Content-Type" not in r.headers:
        return "not_found"

    if "Content-Length" not in r.headers:
        return "not_found"

    if r.headers["Content-Length"] == "8183":
        image_md5 = hashlib.md5(r.content).hexdigest()
        if image_md5 == "0bc8d04776c8eac2a12568d109162249":
            return "not_found"

    return "ok"

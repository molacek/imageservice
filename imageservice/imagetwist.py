import hashlib
import requests
import time
import random
import string
from bs4 import BeautifulSoup
from . import utils


class Imagetwist:

    def __init__(self, username=None, password=None, proxies=None):
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

        self._balance = None
        self._files_count = None
        self._used_space = None

        if proxies:
            self.session.proxies.update(proxies)

        return

    def _login(self):

        if self.logged_in:
            return

        while True:
            try:
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
            except requests.exceptions.ConnectionError:
                print("Connection error when logging in into Imagetwist. "
                      "Will try again in 10 seconds")
                time.sleep(10)
                continue

            break

        bs = BeautifulSoup(r.text, 'html.parser')
        if not bs:
            print("Login failed")
            return False

        self.sess_id = bs.find('input', {'name': 'sess_id'})["value"]
        self.action = bs.find('form', {'name': 'file'})["action"]
        return True

    def _random_filename(self, length=8):
        letters = string.ascii_lowercase
        fn = ''.join(random.choice(letters) for i in range(length))
        return "{0:s}.jpg".format(fn)

    def _prepare_upload_file(self, filename, filesize=6000000, force=False):
        upload_file = {
            "file_0": (
                self._random_filename(),
                utils.image_buffer(filename, filesize, force),
                "image/jpeg"
            ),
            "file_1": (
                "",
                "",
                "application/octet-stream"
            )
        }
        return upload_file

    def upload(self, filename):

        if not self.logged_in:
            login_res = self._login()
            if not login_res:
                return False

        # Verify image integrity
        image_integrity_result = utils.verify_integrity(filename)
        if image_integrity_result is not True:
            status, error = image_integrity_result
            print(f"Image integrity error: {error}")
            return(False)

        upload_id = "".join(random.choice(string.digits) for _ in range(12))
        upload_url = "{0:s}{1:s}&js_on=0&utype=reg&" \
            "upload_type=file".format(self.action, upload_id)

        upload_file = self._prepare_upload_file(filename, 6000000)

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

        forced = False
        while True:
            try:
                r = self.session.post(
                    upload_url,
                    headers=self.headers,
                    files=upload_file,
                    data=upload_data
                )
            except requests.exceptions.ConnectionError:
                print("Connection error. Will try again")
                time.sleep(10)
                continue

            except:
                print("Other error. Will try again")
                time.sleep(10)
                continue

            if "<pre>not image at " in r.text:
                if not forced:
                    print("Imagetwist reported an image error. "
                          "Trying to force image processing")
                    upload_file = self._prepare_upload_file(
                        filename, 6000000, True
                    )
                    forced = True
                    continue
                else:
                    print(f"Unable to upload {filename} even after "
                          "forced processing")
                    return False

            break

        bs = BeautifulSoup(r.text, 'html.parser')
        all_divs = bs.find_all('div')
        n = 0
        for div in all_divs:
            if div.text == 'Preview:':
                thumb = all_divs[n+1].find('img')["src"]
                img = all_divs[n+1].find('a')["href"]
                return(thumb, '/'.join(img.split('/')[0:-1]))
            n += 1

        print("Error result")
        print(r.text)

        return(False)

    def _read_my_account(self):

        if not self.logged_in:
            self._login()

        r = self.session.get("https://imagetwist.com/?op=my_account")
        bs = BeautifulSoup(r.text, 'html.parser')

        # Extract balance
        two_buttons_row = bs.find('div', {'class': 'row two_buttons'})

        balance_div = two_buttons_row.find_all(
           'div',
           {'class': 'col-xs-4 blue-bolded'}
        )

        self._balance = float(balance_div[1].text[1:])

        # Extract used space
        all_divs = bs.find_all('div')
        for i, div in enumerate(all_divs):
            if div.text == 'Used space:':
                self._used_space = all_divs[i+1].text.split('\n')[1].strip()
                break

    def _read_my_files(self):

        if not self.logged_in:
            self._login()

        r = self.session.get("https://imagetwist.com/?op=my_files")
        bs = BeautifulSoup(r.text, 'html.parser')

        # Extract files count
        small = bs.find('small').text
        self._files_count = small[1:-7]

    def balance(self):

        if self._balance is None:
            self._read_my_account()

        return(self._balance)

    def used_space(self):

        if self._used_space is None:
            self._read_my_account()

        return(self._used_space)

    def files_count(self):

        if self._files_count is None:
            self._read_my_files()

        return(self._files_count)

    def validate(self, thumb_url):

        valid_schema = thumb_url.startswith("http://") or thumb_url.startswith("https://")

        if not valid_schema:
            return "invalid_schema"

        while True:
            try:
                r = self.session.get(thumb_url)
            except requests.exceptions.ConnectionError:
                print("Error connecting to {0:s}".format(thumb_url))
                time.sleep(10)
                continue
            except requests.exceptions.ReadTimeout:
                print("Read timeout for {0:s}".format(thumb_url))
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

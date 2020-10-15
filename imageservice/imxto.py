import hashlib
import imageservice
import requests
from . import httpclient
from . import utils

from bs4 import BeautifulSoup


class Imxto:
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

    def _login(self):
        print("Logging into imx.to ...")
        resp = self.http.post(
            "https://imx.to/login.php",
            data={
                "usr_email": self.username,
                "pwd": self.password,
                "doLogin": "Login"
            },
        )
        if "<h1>Welcome " in resp.text:
            return True
        return False

    def _prepare_upload_file(self, file_path):
        upload_file = {
            "uploaded": (
                file_path.parts[-1],
                utils.image_buffer(file_path),
                "image/jpeg"
            )
        }
        return upload_file
    
    def _valid_url_schema(self, url):
        return(url.startswith("http://") or url.startswith("https://"))

    def get_image_url(self, url):
        payload = {"imgContinue": "Continue to image ..."}
        r = requests.post(url, data=payload)
        soup = BeautifulSoup(r.text, "html.parser")
        image_elements = soup.find_all("img", attrs={"class": "centred"})
        image_element = image_elements[0]
        url = image_element["src"]
        file_name = image_element["alt"]
        return(True, (url, file_name))

    def upload(self, file_path):
        if not self.logged_in:
            if not self._login():
                self.status = False
                self.error = "login_failed"
                return self
            self.logged_in = True

        data = {
            "thumb_size_contaner": 3,
            "thumbnail_format": 2,
            "set_galery": "",
            "simple_upload": "Upload"
        }

        files = self._prepare_upload_file(file_path)

        resp = self.http.post(
            "https://imx.to/upload.php",
            data=data,
            files=files
        )

        if "has been succesfuly uploaded " not in resp.text:
            self.status = False
            self.error = "upload_not_confirmed"
            return self

        bs = BeautifulSoup(resp.text, "html.parser")
        upload_div = bs.find("div", {"id": "accordion"})

        if not upload_div:
            self.status = False
            self.error = "missing_image_links"
            return self

        thumb = upload_div.find("img")
        if not thumb:
            self.status = False
            self.error = "missing_upload_thumb"
            return self

        self.thumbnail = thumb["src"]
        parent_link = thumb.parent
        self.image = parent_link["href"]
        self.status = True

        return self

    
    def validate(self, thumb_url):

        status = imageservice.ValidateStatus(False)

        if not self._valid_url_schema(thumb_url):
            status.error = "invalid_schema"
            return status

        r = self.http.get(thumb_url)

        if r.status_code == 404:
            status.error = "not_found"
            return status

        if "Content-Type" not in r.headers:
            status.error = "not_found"
            return status

        if "Content-Length" not in r.headers:
            status.error = "not_found"
            return status

        if r.headers["Content-Length"] == "8183":
            image_md5 = hashlib.md5(r.content).hexdigest()
            if image_md5 == "0bc8d04776c8eac2a12568d109162249":
                status.error = "not_found"
                return status

        status.status = True
        return status
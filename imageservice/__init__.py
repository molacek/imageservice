"""Upload and validate images"""
import requests
import time
from . import imxto, imagebam, pimpandhost, imagetwist, pixhost, imgbox
from . import turboimagehost
from pathlib import PosixPath


class DownloadStatus:
    def __init__(self, status=None, error=None):
        self.status = status
        self.error = error


class Uploader:
    def __init__(self, service, username, password, proxy):
        self.status = True
        self.error = None
        self.proxy = None
        self.username = username
        self.password = password
        self.proxy = proxy
        self.service = service

        if service == "imxto":
            self.service = imxto.Imxto(username, password, proxy)
        elif service == "imagetwist":
            self.service = imagetwist.Imagetwist(username, password, proxy)
        else:
            raise Exception("non_existing_service")

    def upload(self, file_path):
        # Check if file exists
        file_path = PosixPath(file_path)
        if not file_path.is_file():
            self.status = False
            self.error = "file_not_found"
            return self

        return self.service.upload(file_path)


class ValidateStatus:
    def __init__(self, status=None, error=None):
        self.status = status
        self.error = error


def download(url, path=None):
    if url.startswith("https://imx.to/"):
        image_service = imxto.Imxto()
        (status, image_data) = image_service.get_image_url(url)
    elif url.startswith("http://www.imagebam.com/") or url.startswith("https://www.imagebam.com/"):
        image_service = imagebam.Imagebam()
        (status, image_data) = image_service.get_image_url(url)
    elif url.startswith("https://pimpandhost.com"):
        (status, image_data) = pimpandhost.get_image_url(url)
    elif url.startswith("https://pixhost.to"):
        (status, image_data) = pixhost.get_image_url(url)
    elif url.startswith("https://www.turboimagehost.com"):
        (status, image_data) = turboimagehost.get_image_url(url)
    elif url.startswith("https://imgbox.com"):
        (status, image_data) = imgbox.get_image_url(url)
    elif (url.startswith("https://imagetwist.com")
          or url.startswith("http://imagetwist.com")
          or url.startswith("https://error")):
        it = imagetwist.Imagetwist()
        result = it.get_image(url)
        if not result.status:
            return result

        if not path:
            path = result.filename

        with open(path, 'wb') as f:
            f.write(result.image)

        return result

    else:
        print("Cannot find image service for downloading {0:s}".format(url))
        return(DownloadStatus(False, "invalid_image_service"))

    if not status:
        print("Error extracting image from {0:s}".format(url))
        return(False)

    (image_url, file_name) = image_data

    if PosixPath(file_name).is_file():
        print("Image", file_name, "already downloaded")
        return

    while True:
        try:
            r = requests.get(image_url, timeout=60)
        except requests.exceptions.ConnectionError:
            print("Error connecting to {0:s}".format(image_url))
            time.sleep(10)
            continue
        except requests.exceptions.ConnectionResetError:
            print("Connection reset when downloading {0:s}".format(image_url))
            time.sleep(10)
            continue

        break

    with open(file_name, 'wb') as f:
        f.write(r.content)


def validate(thumb_url, sess=None):
    """Validate image status on server

    Params:
        thumb_url - url of the image thumbnail

    Result codes:
        "ok" - image exists
        "not_found" - image has been removed from the server
        "not_implemented - image service not implemented
    """

    if not sess:
        sess = requests.Session()

    if "imagetwist.com" in thumb_url:
        imageservice = imagetwist
    elif "imx.to" in thumb_url:
        imageservice = imxto
    else:
        return "not_implemented"

    return imageservice.validate(thumb_url, sess)

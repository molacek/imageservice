"""Upload and validate images"""
import requests
import time
import sys
from . import imxto, imagebam, pimpandhost, imagetwist, pixhost, imgbox
from . import turboimagehost


def download(url, path=None):

    if url.startswith("https://imx.to/"):
        (status, image_data) = imxto.get_image_url(url)
    elif url.startswith("http://www.imagebam.com/"):
        (status, image_data) = imagebam.get_image_url(url)
    elif url.startswith("https://pimpandhost.com"):
        (status, image_data) = pimpandhost.get_image_url(url)
    elif url.startswith("https://pixhost.to"):
        (status, image_data) = pixhost.get_image_url(url)
    elif url.startswith("https://www.turboimagehost.com"):
        (status, image_data) = turboimagehost.get_image_url(url)
    elif url.startswith("https://imgbox.com"):
        (status, image_data) = imgbox.get_image_url(url)
    elif url.startswith("https://imagetwist.com"):
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

        return(False)

    if not status:
        print("Error extractiong image from {0:s}".format(url))
        return(False)

    (image_url, file_name) = image_data

    while True:
        try:
            r = requests.get(image_url)
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
    else:
        return "not_implemented"

    return imageservice.validate(thumb_url, sess)


def upload(service, filename):
    if service == "imagetwist":
        upload_module = imagetwist
    else:
        print("ERROR: Unknown service: {0:s}".format(service))
        return False
    return upload_module.upload(filename)

"""Upload and validate images"""
import requests
from . import imxto, imagebam, pimpandhost, imagetwist


def download(url, path=None):

    if url.startswith("https://imx.to/"):
        (status, image_data) = imxto.get_image_url(url)
    elif url.startswith("http://www.imagebam.com/"):
        (status, image_data) = imagebam.get_image_url(url)
    elif url.startswith("https://pimpandhost.com"):
        (status, image_data) = pimpandhost.get_image_url(url)
    else:
        print("Cannot find image servis for downloading {0:s}".format(url))

        return(False)

    if not status:
        print("Error extractiong image from {0:s}".format(url))
        return(False)

    (image_url, file_name) = image_data

    r = requests.get(image_url)
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

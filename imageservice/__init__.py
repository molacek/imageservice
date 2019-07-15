import requests
from . import imxto, imagebam, pimpandhost


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

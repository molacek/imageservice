import requests
from bs4 import BeautifulSoup


def get_image_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image = soup.find('img', {'id': 'uImage'})
    if not image:
        return(False, "Unable to find image on {0:s}".format(url))

    return(True, (image["src"], image["src"].split('/')[-1]))

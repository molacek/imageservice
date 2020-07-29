import requests
import time


class HttpClient:
    def __init__(self, proxy=None):
        user_agent = (
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
            "51.0.2683.0 Safari/537.36"
        )

        self.session = requests.Session()
        self.session.headers.update({
            "user-agent": user_agent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/webp,*/*;q=0.8",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1"
        })
        self.proxies = {
            "http": proxy,
            "https": proxy
        }

    def post(self, url, data=None, files=None):
        while True:
            try:
                return(
                    self.session.post(
                        url,
                        timeout=60,
                        data=data,
                        files=files,
                        proxies=self.proxies)
                )
            except requests.exceptions.ConnectionError:
                print("Connection error. Will try again")
                time.sleep(10)
                continue

            except Exception as e:
                print("Other error. Will try again")
                print(e)
                self.logged_in = False
                time.sleep(10)
                continue

    def get(self, url):
        while True:
            try:
                return(
                    self.session.get(
                        url,
                        timeout=60,
                        proxies=self.proxies)
                )
            except requests.exceptions.ConnectionError:
                print("Connection error. Will try again")
                time.sleep(10)
                continue

            except Exception as e:
                print("Other error. Will try again")
                print(e)
                time.sleep(10)
                continue

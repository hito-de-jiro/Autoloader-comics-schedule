import os
import requests

from bs4 import BeautifulSoup

HOST = 'https://moonbeard.com/'
URL = 'https://moonbeard.com/'

os.makedirs('moonbeard_downloads', exist_ok=True)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

fetch = (
    "https://api-public.addthis.com/url/serviceapi/shares-post.json?services=sFbt&url=https%3A%2F%2Fmoonbeard.com%2F",
    {
        "headers": {
            "accept": "*/*",
            "accept-language": "en,en-US;q=0.9",
            "cache-control": "no-cache",
            "content-type": "text/plain",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "cookie": "ouid=63247bb30001c2242af3f585a67ed02e7adae8043e6150702acf; uid=63247bb3302b329b; na_id=2022091613354724000085428825; loc=MDAwMDBFVVVBMTgyMzA4MjA5MzAwMDAwMDBDSA==; mus=0; uvc=9%7C37%2C12%7C38",
            "Referer": "https://moonbeard.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        },
        "body": '',
        "method": "POST"
    }
)

def get_html(url=URL):
    res = requests.post(url)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('Something wrong. Error %s' % exc)
    finally:
        print(res.text)

    return res


def main(url):
    get_html(url)


if __name__ == '__main__':
    main(URL)

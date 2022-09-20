import os
import time
import requests

from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36',
}
URL = 'http://www.lunarbaboon.com/'
os.makedirs('lunarbaboon_downloads', exist_ok=True)


def get_html(url=URL, headers=HEADERS):
    res = requests.get(url, headers)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('Something wrong! Error %s ' % exc)

    return res.text


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


def main():
    html = get_html(URL, HEADERS)
    get_content(html)


if __name__ == '__main__':
    main()

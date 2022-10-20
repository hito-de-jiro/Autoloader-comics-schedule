import os
import time

import requests

from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36',
}

HOST = 'http://www.lunarbaboon.com'
os.makedirs('lunarbaboon_downloads', exist_ok=True)


def get_html(url=HOST):
    """"""
    sess = requests.Session()

    while True:
        res = sess.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comics_urls = get_comics_urls(soup)
        for comic_url in comics_urls:
            file_name = os.path.basename(comic_url).split('?')[0]
            has_comic = _save_comic(comic_url, file_name)
            if not has_comic:
                print('Done')
                return

        time.sleep(1)
        url = get_next_page(soup)


def get_comics_urls(soup):
    """"""
    comics_urls = []
    items = soup.select('.body>p>span>img')
    for item in items:
        if not item:
            continue
        else:
            image_link = item.get('src')
            comic_url = HOST + image_link
            comics_urls.append(comic_url)

    return comics_urls


def get_next_page(soup):
    """"""
    next_page = soup.select('.paginationControlNextPageSuffix>a')[0]
    url = HOST + next_page.get('href')
    return url


def _save_comic(comic_url, file_name, headers=HEADERS):
    """"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join('lunarbaboon_downloads', file_name)
    if not os.path.isfile(image_path):
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print('No new comics!')
        return False


def main():
    """"""
    # url = 'http://www.lunarbaboon.com/comics/?currentPage=195'
    get_html(url=HOST)


if __name__ == '__main__':
    main()

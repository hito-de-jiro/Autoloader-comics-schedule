import os
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
    """"Get html of page for parsing"""
    sess = requests.Session()

    while True:
        res = sess.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comics_urls = get_comics_urls(soup)
        # print(comics_urls)
        for comic_url in comics_urls:
            file_name = os.path.basename(comic_url).split('?')[0]
            has_comic = _save_comic(comic_url, file_name)
            if not has_comic:
                return
        try:
            url = get_next_page(soup)
        except IndexError:
            print('Done!')
            return


def get_comics_urls(soup):
    """Get all URLs from page"""
    comics_urls = []
    items = soup.select('.body')
    for item in items:
        if not item:
            continue
        else:
            image_link = item.find_all('img')[0].get('src')
            if image_link.startswith('http://'):
                comic_url = image_link
            else:
                comic_url = HOST + image_link
            comics_urls.append(comic_url)

    return comics_urls


def get_next_page(soup):
    """Get a URL for next page"""
    url = HOST + soup.select('.paginationControlNextPageSuffix>a')[0].get('href')
    return url


def _save_comic(comic_url, file_name, headers=HEADERS):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join('lunarbaboon_downloads', file_name)
    # checking file availability
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
    """Start the main process"""
    try:
        # this a last page
        url = 'http://www.lunarbaboon.com/comics/?currentPage=195'
        get_html(url)
    except KeyboardInterrupt:
        print('Forced program termination!')
        return


if __name__ == '__main__':
    main()

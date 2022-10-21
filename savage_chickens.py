import os
import time
import requests

from bs4 import BeautifulSoup

HOST = 'https://www.savagechickens.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36',
}
os.makedirs('comics_folder/chickens', exist_ok=True)


def get_html(url=HOST):

    while True:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comic_urls = get_comics_urls(soup)
        for comic_url in comic_urls:
            has_comic = save_comic(comic_url)
            if not has_comic:
                return
        try:
            url = get_next_page(soup)
        except IndexError:
            print('Done!')
            return


def get_next_page(soup):
    """Get a URL for next page"""
    url = soup.select('.previous-entries>a')[0].get('href')
    return url


def save_comic(comic_url):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url)
    res.raise_for_status()
    image_file_path = os.path.join('comics_folder/chickens', os.path.basename(comic_url))

    if not os.path.isfile(image_file_path):
        print('Download image... %s' % comic_url)
        image_file = open(image_file_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print('No new comics!')
        return False


def get_comics_urls(soup):
    """Get all URLs from page"""
    comics_urls = []
    items = soup.select('.entry_content>p>img')
    for item in items:
        if not item:
            continue
        else:
            image_link = item.get('src')
            comics_urls.append(image_link)
    return comics_urls


def main():
    """Start the main process"""
    try:
        # this a last page
        # url = 'https://www.savagechickens.com/page/1182'
        get_html()
    except KeyboardInterrupt:
        print('Forced program termination!')
        return


if __name__ == '__main__':
    main()

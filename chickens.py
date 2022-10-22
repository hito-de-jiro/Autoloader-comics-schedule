import argparse
import os
import requests

from bs4 import BeautifulSoup

HOST = 'https://www.savagechickens.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36',
}
os.makedirs('comics_folder/chickens', exist_ok=True)


def get_html(comics_folder, url=HOST):
    while True:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comic_urls = get_comics_urls(soup)
        for comic_url in comic_urls:
            has_comic = save_comic(comic_url, comics_folder)
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


def save_comic(comic_url, comics_folder):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url)
    res.raise_for_status()
    image_file_path = os.path.join(comics_folder, os.path.basename(comic_url))

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


def main(comics_folder):
    """Start the main process"""
    print('Chickens start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.savagechickens.com/page/1182'
        get_html(comics_folder)
    except KeyboardInterrupt:
        print('Forced <Savage_chickens> program termination!')
        return


def choice_folder() -> str:
    """Choice output comics folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    args = parser.parse_args()

    default_path = 'comics_folder/chickens'
    outdir = args.outdir
    if outdir is None:
        return default_path
    elif os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


if __name__ == '__main__':
    main(comics_folder=choice_folder())

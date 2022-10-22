import argparse
import os
import requests

from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36',
}

HOST = 'http://www.lunarbaboon.com'
os.makedirs('comics_folder/lunarbaboon', exist_ok=True)


def get_html(comics_folder, url=HOST):
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
            has_comic = save_comic(comic_url, comics_folder, file_name)
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


def save_comic(comic_url, comics_folder, file_name, headers=HEADERS):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join(comics_folder, file_name)
    # checking file availability
    if not os.path.isfile(image_path):
        print('Download image... %s' % comic_url.split('?')[0])
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print('No new comics!')
        return False


def main(comics_folder):
    """Start the main process"""
    print('Lunarbaboon start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'http://www.lunarbaboon.com/comics/?currentPage=195'
        get_html(comics_folder)
    except KeyboardInterrupt:
        print('Forced <Lunarbaboon> program termination!')
        return


def choice_folder() -> str:
    """Choice output comics folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    args = parser.parse_args()

    default_path = 'comics_folder/lunarbaboon'
    outdir = args.outdir
    if outdir is None:
        return default_path
    elif os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


if __name__ == '__main__':
    main(comics_folder=choice_folder())

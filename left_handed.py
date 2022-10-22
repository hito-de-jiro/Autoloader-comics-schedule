import argparse
import os
import requests

from bs4 import BeautifulSoup

HOST = 'http://www.lefthandedtoons.com/'
os.makedirs('comics_folder/left_handed', exist_ok=True)


def get_html(comics_folder, url=HOST):
    while True:
        #  завантаженя сторінки
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'lxml')
        comic_elem = soup.select('.comicimage')
        if not comic_elem:
            print('Image not found')
        else:
            comic_url = comic_elem[0].get('src')
            has_comic = save_comic(comic_url, comics_folder)
            if not has_comic:
                return
        try:
            url = prev_link(soup)
        except IndexError:
            print('Done!')
            break


def save_comic(comic_url, comics_folder):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url)
    res.raise_for_status()
    image_path = os.path.join(comics_folder, os.path.basename(comic_url))
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


def prev_link(soup):
    """Get a URL preview link"""
    url = HOST + soup.select('.prev>a')[0].get('href')
    return url


def main(comics_folder):
    """Start the main process"""
    print('Left_handed start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.lefthandedtoons.com/1/'
        get_html(comics_folder)
    except KeyboardInterrupt:
        print('Forced <left_handed_toons> program termination!')
        return


def choice_folder() -> str:
    """Choice output comics folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    args = parser.parse_args()

    default_path = 'comics_folder/left_handed'
    outdir = args.outdir
    if outdir is None:
        return default_path
    elif os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


if __name__ == '__main__':
    main(comics_folder=choice_folder())

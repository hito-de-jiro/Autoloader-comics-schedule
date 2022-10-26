import argparse
import datetime
import os
import requests

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

HOST = 'http://www.lefthandedtoons.com/'
DEFAULT_PATH = 'comics_folder/left_handed'


def get_html(comics_folder, date_limit, url=HOST):
    while True:
        #  завантаженя сторінки
        sess = requests.Session()
        res = sess.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'lxml')

        comic_elem = soup.select('.comicimage')
        comic_date = soup.find('div', class_='comictitlearea').getText().split('\n')[1]
        comic_date = parse_date(comic_date)

        if not comic_elem:
            print('Image not found')
        else:
            comic_url = comic_elem[0].get('src')

            if date_limit and comic_date < date_limit:
                print(f'Done. Got date limit')
                return

            save_comic(comic_url, comics_folder, comic_date)

        try:
            url = prev_link(soup)
        except IndexError:
            print('Done!')
            break


def save_comic(comic_url, comics_folder, comic_date: datetime):
    """Get URL of image and save file in base folder"""
    sess = requests.Session()
    res = sess.get(comic_url)
    res.raise_for_status()
    comic_name = comic_date.strftime("%Y-%m-%d") + '__' + os.path.basename(comic_url)
    image_path = os.path.join(comics_folder, comic_name)
    # checking file availability
    if not os.path.isfile(image_path):
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print(f'Date: {comic_date.strftime("%Y-%m-%d")} -- No new comics!')
        return False


def prev_link(soup):
    """Get a URL preview link"""
    url = HOST + soup.select('.prev>a')[0].get('href')
    return url


def parse_comic_date(soup) -> datetime:
    """Get the publication date of the comic"""
    date_comic = soup.select('#headernav-date')[0].getText()
    comic_date = parse_date(date_comic.strip())
    return comic_date


def main(comics_folder, date_limit):
    """Start the main process"""
    print('Left_handed start')
    print(f'Comics folder is {comics_folder}')

    if date_limit:
        print(f'Date limit is {date_limit}')

    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.lefthandedtoons.com/1/'
        get_html(comics_folder, date_limit)
    except KeyboardInterrupt:
        print('Forced <left_handed_toons> program termination!')
        return


def valid_date(s):
    """Datetime validator"""
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_params():
    """Choice output comics folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    parser.add_argument('--date_limit', type=valid_date,
                        default=None, help="The Date - format YYYY-MM-DD")
    args = parser.parse_args()

    if args.outdir is None:
        args.outdir = DEFAULT_PATH
    elif not os.path.isabs(args.outdir):
        raise ValueError('Path is not absolute')

    return args


if __name__ == '__main__':
    params = parse_params()
    main(comics_folder=params.outdir, date_limit=params.date_limit)

# TODO: проверить работоспособность
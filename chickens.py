import argparse
import datetime
import os
import requests

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

HOST = 'https://www.savagechickens.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36',
}
DEFAULT_PATH = 'comics_folder/chickens'


def get_html(comics_folder, date_limit: datetime, url=HOST):
    while True:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        if date_limit:
            print(f'Date limit is {date_limit}')

        comics_dict = get_content(soup)
        for comic_date, comic_url in comics_dict.items():

            comic_date = parse_date(comic_date, ignoretz=True)
            print(comic_date)
            if date_limit and comic_date < date_limit:
                print(f'Done. Got date limit')
                return
            save_comic(comic_url, comics_folder, comic_date)

        try:
            url = get_next_page(soup)
        except IndexError:
            print('Done!')
            return


def get_next_page(soup):
    """Get a URL for next page"""
    url = soup.select('.previous-entries>a')[0].get('href')
    return url


def save_comic(comic_url, comics_folder, comic_date):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url)
    res.raise_for_status()
    comic_name = comic_date.strftime("%Y-%m-%d") + '_' + os.path.basename(comic_url)
    image_file_path = os.path.join(comics_folder, comic_name)

    if not os.path.isfile(image_file_path):
        print('Download image... %s' % comic_url)
        image_file = open(image_file_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print(f'Date: {comic_date.strftime("%Y-%m-%d")} -- No new comics!')
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


def get_content(soup) -> dict:
    """Return dict: k - date, v - url"""
    comic_urls = []
    comic_dates = []
    items = soup.select('.copy-pad')

    for item in items:
        images = item.select('div[id]')
        elems = item.select('span[title]')
        for image in images:
            comic_url = (image.find('img').get('src'))
            comic_urls.append(comic_url)
        for elem in elems:
            comic_date = elem.get('title')
            comic_dates.append(comic_date)
    find_elems = dict(zip(comic_dates, comic_urls))

    return find_elems


def main(comics_folder, date_limit):
    """Start the main process"""
    print('Chickens start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.savagechickens.com/page/1182'
        get_html(comics_folder, date_limit)
    except KeyboardInterrupt:
        print('Forced <Savage_chickens> program termination!')
        return


def valid_date(s):
    """Datetime validator"""
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_params():
    """Parser parametrs CLI"""
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

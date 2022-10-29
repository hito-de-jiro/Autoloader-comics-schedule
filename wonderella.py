import datetime
import argparse
import os
import requests

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

HOST = 'http://nonadventures.com/'
DEFAULT_PATH = 'comics_folder/wonderella'
START_TIME = datetime.datetime.now()
DEFAULT_DATE = (START_TIME - datetime.timedelta(days=30)).strftime("%Y-%m-%d")


def get_html(comics_folder, date_limit: datetime, url=HOST):
    """"Get html of page for parsing"""
    while True:
        sess = requests.Session()
        res = sess.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comics_dict = get_content(soup)

        for comic_date, comic_url in comics_dict.items():

            if date_limit and comic_date < date_limit:
                print(f'Done. Got date limit.')
                return
            save_comic(comic_url, comics_folder, comic_date)

        try:
            url = prev_link(soup)
        except IndexError:
            print('Done!')
            return


def get_content(soup) -> dict:
    """Return dict: k - date, v - url"""
    content_dict = {}
    date = get_comic_date(soup)
    link = get_comic_url(soup)
    content_dict[date] = link
    return content_dict


def save_comic(comic_url, comics_folder, comic_date) -> bool:
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
    url = soup.select('.nav>a[rel="prev"]')[0].get('href')

    return url


def get_comic_date(soup) -> datetime:
    """Get the publication date of the comic"""
    date = soup.find('div', class_="comicdate").getText()
    date_comic = date.split('\n')[-1].strip()
    date_comic = parse_date(date_comic.split('—')[-1])

    return date_comic


def get_comic_url(soup):
    """Get the link for download of the comic"""
    link = soup.select('#comic>img')[0].get('src')

    return link


def main(comics_folder, date_limit):
    """Start the main process"""
    print('<Wonderella> start!')
    print(f'Comics folder is {comics_folder}')

    if date_limit:
        print(f'Date limit is {date_limit.strftime("%Y-%m-%d")}')

    os.makedirs(comics_folder, exist_ok=True)
    try:
        get_html(comics_folder, date_limit)
    except KeyboardInterrupt:
        print('Forced <wonderella> program termination!')
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

    if args.date_limit is None:
        args.date_limit = parse_date(DEFAULT_DATE)

    return args


if __name__ == '__main__':
    params = parse_params()
    main(comics_folder=params.outdir, date_limit=params.date_limit)

import argparse
import datetime
import os
import requests

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

HOST = 'https://www.exocomics.com'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
DEFAULT_PATH = 'comics_folder/exocomics'
START_TIME = datetime.datetime.now()
DEFAULT_DATE = (START_TIME - datetime.timedelta(days=30)).strftime("%Y-%m-%d")


def get_html(comics_folder, date_limit, url=HOST):
    """"Get html of page for parsing"""
    sess = requests.Session()
    while True:
        res = sess.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')

        try:
            comic_link = soup.find('img', class_='image-style-main-comic').get('src')
            comic_url = HOST + comic_link
            comic_date = soup.find('div', class_='date').getText()
            # print(comic_date)
            comic_date = parse_date(comic_date)

            if date_limit and comic_date < date_limit:
                print(f'Done. Got date limit')
                return

            save_comic(comic_url, comics_folder, comic_date)
        except AttributeError:
            continue

        finally:
            prev_link = _prev_url(soup)
            url = HOST + prev_link
        if prev_link == '':
            print('Done!')
            return


def save_comic(comic_url, comics_folder, comic_date, headers=HEADERS):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    comic_name = comic_date.strftime("%Y-%m-%d") + '__' + os.path.basename(comic_url)
    image_path = os.path.join(comics_folder, comic_name)
    if not os.path.isfile(image_path):  # Перевірка існування файлу.
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print(f'Date: {comic_date.strftime("%Y-%m-%d")} -- No new comics!')
        return False


def _prev_url(soup):
    """Get a URL preview link"""
    try:
        prev_link = soup.find('a', class_='ir prev').get('href')
    except AttributeError:
        prev_link = ''
    return prev_link


def main(comics_folder, date_limit):
    """Start the main process"""
    print('Exocomic start')
    print(f'Comics folder is {comics_folder}')

    if date_limit:
        print(f'Date limit is {date_limit.strftime("%Y-%m-%d")}')

    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.exocomics.com/500/'
        get_html(comics_folder, date_limit)
    except KeyboardInterrupt:
        print('Forced <exocomic> program termination!')
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


if __name__ == "__main__":
    params = parse_params()
    main(comics_folder=params.outdir, date_limit=params.date_limit)

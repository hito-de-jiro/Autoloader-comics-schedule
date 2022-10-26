import datetime
import argparse
import requests
import os

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

HOST = 'https://www.buttersafe.com/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
COOKIES = {
    'cookie': '__utmc=170251443; __utmz=170251443.1663335330.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
              '__utma=170251443.1798268114.1663335330.1663658480.1663662984.10; __utmt=1; '
              '__utmb=170251443.1.10.1663662984; __atuvc=9%7C37%2C20%7C38; __atuvs=63297b88232b3e2b000'
}
DEFAULT_PATH = 'comics_folder/buttersafe'


def get_html(comics_folder, date_limit: datetime, url=HOST):
    """"Get html of page for parsing"""
    while True:
        sess = requests.Session()
        res = sess.get(url, headers=HEADERS, cookies=COOKIES)
        soup = BeautifulSoup(res.text, 'lxml')

        comic_elems = soup.select('#comic')
        for item in comic_elems:
            if not comic_elems and not date_limit:
                print('Image not found')
            else:
                comic_url = item.find('img').get('src')
                comic_date = parse_comic_date(soup)  # return comic date in datetime type

                if date_limit and comic_date < date_limit:
                    print(f'Done. Got date limit')
                    return

                save_comic(comic_url, comics_folder, comic_date)

        try:
            url = prev_link(soup)
        except IndexError:
            print('Done!')
            return


def save_comic(comic_url, comics_folder, comic_date: datetime) -> bool:
    """Get URL of image and save file in base folder"""
    sess = requests.Session()
    res = sess.get(comic_url, headers=HEADERS, cookies=COOKIES)
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
    url = soup.select('#headernav>a[rel="prev"]')[0].get('href')
    return url


def parse_comic_date(soup) -> datetime:
    """Get the publication date of the comic"""
    date_comic = soup.select('#headernav-date')[0].getText()
    comic_date = parse_date(date_comic.strip())
    return comic_date


def main(comics_folder, date_limit):
    """Start the main process"""
    print('Buttersafe start')
    print(f'Comics folder is {comics_folder}')

    if date_limit:
        print(f'Date limit is {date_limit}')

    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.buttersafe.com/2007/04/03/breakfast-sad-turtle/'
        # date_limit = datetime.strptime(date_limit, "%Y-%m-%d")  # convert str to datetime
        get_html(comics_folder, date_limit)
    except KeyboardInterrupt:
        print('Forced <buttersafe> program termination!')
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


if __name__ == "__main__":
    params = parse_params()
    main(comics_folder=params.outdir, date_limit=params.date_limit)

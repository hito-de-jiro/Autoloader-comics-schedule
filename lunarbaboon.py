import argparse
import datetime
import os
import requests

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

HOST = 'http://www.lunarbaboon.com'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/106.0.0.0 Safari/537.36',
}
COOKIES = {
    'Cookie': 'JSESSIONID=4671D41BC6A297E8F70576727EA7D0F9.v5-web010; '
              'ss_cid=f051e213-4199-4184-b464-9b958402c8b3; ss_cpvisit=1663317626270; '
              'ss_cid=f051e213-4199-4184-b464-9b958402c8b3; ss_cpvisit=1666782210676'
}
DEFAULT_PATH = 'comics_folder/lunarbaboon'
START_TIME = datetime.datetime.now()
DEFAULT_DATE = (START_TIME - datetime.timedelta(days=30)).strftime("%Y-%m-%d")


def get_html(comics_folder, date_limit: datetime, url=HOST):
    """"Get html of page for parsing"""
    sess = requests.Session()

    while True:
        res = sess.get(url, headers=HEADERS, cookies=COOKIES)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comics_dict = get_content(soup)
        for comic_date, comic_url in comics_dict.items():
            if date_limit and comic_date < date_limit:
                print('Done. Got date limit')
                return
            save_comic(comic_url, comics_folder, comic_date)

        try:
            url = get_next_page(soup)
        except IndexError:
            print('Done!')
            return


def get_content(soup) -> dict:
    """Return dict: k - date, v - url"""
    global comic_images_elem
    comic_urls = []
    comic_dates = []
    if soup.select('.body>p>span>span>img'):
        comic_images_elem = soup.select('.body>p>span>span>img')
    elif soup.select('.body>p>span>img'):
        comic_images_elem = soup.select('.body>p>span>img')
    comic_dates_elem = soup.select('.posted-on')
    for image in comic_images_elem:
        image_link = image.get('src')
        if image_link.startswith('http://'):
            comic_url = image_link
        else:
            comic_url = HOST + image_link
        comic_urls.append(comic_url)

    for date in comic_dates_elem:
        comic_date = date.getText()
        comic_date = parse_date(comic_date)

        comic_dates.append(comic_date)

    find_elems = dict(zip(comic_dates, comic_urls))

    return find_elems


def get_next_page(soup):
    """Get a URL for next page"""
    url = HOST + soup.select('.paginationControlNextPageSuffix>a')[0].get('href')
    return url


def save_comic(comic_url, comics_folder, comic_date):
    """Get URL of image and save file in base folder"""
    comic_link = comic_url.split('?')[0]
    sess = requests.Session()
    res = sess.get(comic_link, headers=HEADERS, cookies=COOKIES)
    res.raise_for_status()
    file_name = comic_date.strftime("%Y-%m-%d") + '__' + os.path.basename(comic_url).split('?')[0]
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
        print(f'Date: {comic_date.strftime("%Y-%m-%d")} -- No new comics!')
        return False


def main(comics_folder, date_limit):
    """Start the main process"""
    print('Lunarbaboon start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'http://www.lunarbaboon.com/comics/?currentPage=195'
        get_html(comics_folder, date_limit)
    except KeyboardInterrupt:
        print('Forced <Lunarbaboon> program termination!')
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

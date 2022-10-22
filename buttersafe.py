import requests
import os
import argparse

from bs4 import BeautifulSoup

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


def get_html(comics_folder, url=HOST):
    """"Get html of page for parsing"""
    while True:
        res = requests.get(url, headers=HEADERS, cookies=COOKIES)
        soup = BeautifulSoup(res.text, 'lxml')
        comic_elems = soup.select('#comic')
        for item in comic_elems:
            if not comic_elems:
                print('Image not found')
            else:
                print(comic_date(soup))  # return comic date
                comic_url = item.find('img').get('src')
                has_comic = save_comic(comic_url, comics_folder)
                if not has_comic:
                    return
        try:
            url = prev_link(soup)
        except IndexError:
            print('Done!')
            return


def save_comic(comic_url, comics_folder):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url, headers=HEADERS, cookies=COOKIES)
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
    url = soup.select('#headernav>a[rel="prev"]')[0].get('href')
    return url


def comic_date(soup):
    """Get the publication date of the comic"""
    date_comic = soup.select('#headernav-date')[0].getText()
    return date_comic.strip()


def main(comics_folder):
    """Start the main process"""
    print('Buttersafe start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.buttersafe.com/2007/04/03/breakfast-sad-turtle/'
        get_html(comics_folder)
    except KeyboardInterrupt:
        print('Forced <buttersafe> program termination!')
        return


def choice_folder() -> str:
    """Choice output comics folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    args = parser.parse_args()

    default_path = 'comics_folder/buttersafe'
    outdir = args.outdir
    if outdir is None:
        return default_path
    elif os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


if __name__ == "__main__":
    main(comics_folder=choice_folder())

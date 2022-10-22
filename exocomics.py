import os
import requests
import argparse

from bs4 import BeautifulSoup

HOST = 'https://www.exocomics.com'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
os.makedirs('comics_folder/exocomics', exist_ok=True)


def get_html(comics_folder, url=HOST):
    """"Get html of page for parsing"""
    sess = requests.Session()
    while True:
        res = sess.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            item = soup.find('img', class_='image-style-main-comic').get('src')
            comic_url = HOST + item
            has_new_comic = save_comic(comics_folder, comic_url, headers=HEADERS)
            if not has_new_comic:
                return
        except AttributeError:
            print(f"Page {url} -- Image not found")
            continue
        finally:
            prev_link = _prev_url(soup)
            url = HOST + prev_link
        if prev_link == '':
            print('Done!')
            return


def save_comic(comics_folder, comic_url, headers=HEADERS):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join(comics_folder, os.path.basename(comic_url))
    if not os.path.isfile(image_path):  # Перевірка існування файлу.
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print('No new comics!')
        return False


def _prev_url(soup):
    """Get a URL preview link"""
    try:
        prev_link = soup.find('a', class_='ir prev').get('href')
    except AttributeError:
        prev_link = ''
    return prev_link


def main(comics_folder):
    """Start the main process"""
    print('Exocomic start')
    print(f'Comics folder is {comics_folder}')
    os.makedirs(comics_folder, exist_ok=True)
    try:
        # this a last page
        # url = 'https://www.exocomics.com/500/'
        get_html(comics_folder)
    except KeyboardInterrupt:
        print('Forced <exocomic> program termination!')
        return


def choice_folder() -> str:
    """Choice output comics folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    args = parser.parse_args()

    default_path = 'comics_folder/exocomics'
    outdir = args.outdir
    if outdir is None:
        return default_path
    elif os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


if __name__ == "__main__":
    main(comics_folder=choice_folder())

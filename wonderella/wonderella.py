import os
import requests

from bs4 import BeautifulSoup

HOST = 'http://nonadventures.com/'
os.makedirs('wonderella_downloads', exist_ok=True)


def get_html(url=HOST):
    """"Get html of page for parsing"""
    while True:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        comic_elems = soup.select('#comic')
        for item in comic_elems:
            if not comic_elems:
                print('Image not found')
            else:
                comic_url = item.find('img').get('src')
                has_comic = save_comic(comic_url)
                if not has_comic:
                    return
        try:
            url = prev_link(soup)
        except IndexError:
            print('Done!')
            return


def save_comic(comic_url):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url)
    res.raise_for_status()
    image_path = os.path.join('wonderella_downloads', os.path.basename(comic_url))
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
    url = soup.select('.nav>a[rel="prev"]')[0].get('href')
    return url


def main():
    """Start the main process"""
    try:
        # this a last page
        # url = 'http://nonadventures.com/2006/09/09/the-torment-of-a-thousand-yesterdays/'
        get_html()
    except KeyboardInterrupt:
        print('Forced program termination!')
        return


if __name__ == '__main__':
    main()

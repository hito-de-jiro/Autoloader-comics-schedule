import os
import requests
import time

from bs4 import BeautifulSoup

URL = 'https://moonbeard.com'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36',
}
os.makedirs('comics_folder/moonbeard', exist_ok=True)


def get_html(url=URL):
    """"""
    flag = True
    sess = requests.Session()

    while flag:
        res = sess.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            items = soup.select('#comic-1>a>img')
            for item in items:
                if not item:
                    continue
                else:
                    comic_url = item.get('src')
                    print(comic_url)

        except AttributeError:
            print(f"Page {url} -- Image not found")
            continue
        finally:
            time.sleep(2)
            prev_link = _prev_url(soup)
            if prev_link:
                url = prev_link
            else:
                print('Done!')
                flag = False


def _prev_url(soup):
    try:
        prev_link = soup.find('a', class_='navi navi-prev').get('href')
        return prev_link
    except AttributeError:
        return False


def _save_comic(comic_url, headers=HEADERS):
    """Get URL of image and save file in base folder"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join('comics_folder/moonbeard', os.path.basename(comic_url))
    if not os.path.isfile(image_path):  # Checking the existence of the file.
        print('You have a new comics')
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
        return True
    else:
        print('No new comics!')


def main():
    img_link = 'https://moonbeard.com/comics/2022-07-10-MB-2022-07%20Pain.png'
    _save_comic(img_link)


if __name__ == '__main__':
    main()

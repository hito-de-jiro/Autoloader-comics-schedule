import os
import time
import requests

from bs4 import BeautifulSoup

HOST = 'https://www.savagechickens.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36',
}

os.makedirs('savage_chickens_downloads', exist_ok=True)
url = 'https://www.savagechickens.com/page/'
params = ''


def main():
    num_page = 1
    while url:
        res = requests.get(f'{url}{num_page}', headers=HEADERS, params=params)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Something wrong! Error... %s' % exc)
        finally:
            print('Download page #%s' % num_page)
            soup = BeautifulSoup(res.text, 'lxml')
            time.sleep(1)
            items = soup.select('.entry_content>p>img')

            for item in items:
                if not item:
                    continue
                else:
                    image_link = item.get('src')

                res = requests.get(image_link)
                res.raise_for_status()
                image_file_path = os.path.join('savage_chickens_downloads', os.path.basename(image_link))

                if not os.path.isfile(image_file_path):
                    print('Download image... %s' % image_link)
                    image_file = open(image_file_path, 'wb')
                    for chunk in res.iter_content(100_000):
                        image_file.write(chunk)
                    image_file.close()
                else:
                    print('Image exist!')

            num_page += 1
            time.sleep(1)


if __name__ == '__main__':
    main()

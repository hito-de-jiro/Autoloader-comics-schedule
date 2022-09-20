import os
import requests

from bs4 import BeautifulSoup


HOST = 'http://nonadventures.com/'
os.makedirs('wonderella_downloads', exist_ok=True)


def main(url=HOST):

    while True:
        #  завантаженя сторінки
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'lxml')
        comic_elems = soup.select('#comic')

        for item in comic_elems:
            # print(item.find('img').get('src'))
            if comic_elems == []:
                print('Image not found')
            else:
                # print(comic_elems)
                comic_url = item.find('img').get('src')
                # print(comic_url)
                res = requests.get(comic_url)
                res.raise_for_status()
                image_path = os.path.join('wonderella_downloads', os.path.basename(comic_url))

                if not os.path.isfile(image_path):
                    print('Download image... %s' % comic_url)
                    image_file = open(image_path, 'wb')
                    for chunk in res.iter_content(100_000):
                        image_file.write(chunk)
                    image_file.close()
                else:
                    print('Image exist!')

            try:
                nav_elems = soup.select('.nav>a[rel="prev"]')
                url = nav_elems[0].get('href')
            except IndexError:
                print('Done!')
                break


if __name__ == '__main__':
    main()

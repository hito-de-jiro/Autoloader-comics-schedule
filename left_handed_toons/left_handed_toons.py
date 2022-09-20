import os
import requests

from bs4 import BeautifulSoup


URL = 'https://www.lefthandedtoons.com/'
os.makedirs('left_handed_toons_downlods', exist_ok=True)


def main(url=URL):


    while True:
        #  завантаженя сторінки
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'lxml')
        comic_elem = soup.select('.comicimage')
        if comic_elem == []:
            print('Image not found')
        else:
            comic_url = comic_elem[0].get('src')

            res = requests.get(comic_url)
            res.raise_for_status()
            image_path = os.path.join('left_handed_toons_downlods', os.path.basename(comic_url))

            if not os.path.isfile(image_path):
                print('Download image... %s' % comic_url)
                image_file = open(image_path, 'wb')
                for chunk in res.iter_content(100_000):
                    image_file.write(chunk)
                image_file.close()
            else:
                print('Image exist!')

        try:
            prev_link = soup.select('.prev>a')[0]
            url = URL + prev_link.get('href')
        except IndexError:
            print('Done!')
            break


if __name__ == '__main__':
    main()

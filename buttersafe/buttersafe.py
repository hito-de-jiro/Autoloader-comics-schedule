import requests
import os

from bs4 import BeautifulSoup

url = 'https://www.buttersafe.com/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
COOKIES = {
    'cookie': '__utmc=170251443; __utmz=170251443.1663335330.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=170251443.1798268114.1663335330.1663658480.1663662984.10; __utmt=1; __utmb=170251443.1.10.1663662984; __atuvc=9%7C37%2C20%7C38; __atuvs=63297b88232b3e2b000'
}


while True:
    res = requests.get(url, headers=HEADERS, cookies=COOKIES)
    soup = BeautifulSoup(res.text, 'lxml')
    comic_elems = soup.select('#comic')
    for item in comic_elems:
        if comic_elems == []:
            print('Image not found')
        else:
            comic_url = item.find('img').get('src')
            res = requests.get(comic_url, headers=HEADERS, cookies=COOKIES)
            res.raise_for_status()
            image_path = os.path.join('buttersafe_downloads', os.path.basename(comic_url))
            if not os.path.isfile(image_path):
                print('Download image... %s' % comic_url)
                image_file = open(image_path, 'wb')
                for chunk in res.iter_content(100_000):
                    image_file.write(chunk)
                image_file.close()
            else:
                print('Image exist!')

        try:
            nav_elems = soup.select('#headernav>a[rel="prev"]')
            url = nav_elems[0].get('href')
        except IndexError:
            print('Done!')
            break
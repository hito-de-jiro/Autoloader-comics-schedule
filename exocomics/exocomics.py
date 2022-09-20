import os
import requests

from bs4 import BeautifulSoup


url = 'https://www.exocomics.com'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
cookies = {
    ''
}


res = requests.get(url, headers)
res.raise_for_status()
# print(res.text)

soup = BeautifulSoup(res.text, 'lxml')
items = soup.select('img', class_='image-style-main-comic')
print(items)
print(items[0])
link = items[0].get('src')

comic_url = f'{url}{link}'
print(comic_url)

if items == []:
    print('Image not found')
else:
    comic_url = f'{url}{link}'
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join('exocomics_download', os.path.basename(comic_url))
    if not os.path.isfile(image_path):
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
    else:
        print('Image exist!')

# TODO: make get link for prev page (pagenation?)


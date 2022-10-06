import os
import requests

from bs4 import BeautifulSoup

URL = 'https://www.exocomics.com'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


def get_html(url=URL):
    """Отримує URL комікса і передає його на завантаження"""
    flag = True
    sess = requests.Session()
    while flag:
        res = sess.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            item = soup.find('img', class_='image-style-main-comic').get('src')
            comic_url = URL + item
            print(f"Page {comic_url} ...")
            # _save_comic(comic_url, headers=HEADERS)  # Завантаження і перевірка файлу
        except AttributeError:
            print(f"Page {url} -- Image not found")
            continue
        finally:
            prev_link = _prev_url(soup)
            if prev_link:
                url = URL + prev_link
            else:
                print('Done!')
                flag = False


def _prev_url(soup):
    try:
        prev_link = soup.find('a', class_='ir prev').get('href')
    except AttributeError:
        prev_link = False
    return prev_link


def _save_comic(comic_url, headers=HEADERS):
    """Перевіряє наявність і завантажує файл"""
    res = requests.get(comic_url, headers)
    res.raise_for_status()
    image_path = os.path.join('exocomics_download', os.path.basename(comic_url))
    if not os.path.isfile(image_path):  # Перевірка існування файлу.
        print('Download image... %s' % comic_url)
        image_file = open(image_path, 'wb')
        for chunk in res.iter_content(100_000):
            image_file.write(chunk)
        image_file.close()
    else:
        print('Image exist!')


def main():
    get_html()
    print('Aliluya!')


if __name__ == "__main__":
    main()

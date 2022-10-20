import os
import time
import requests

from bs4 import BeautifulSoup

HOST = 'https://www.savagechickens.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

url = 'https://www.savagechickens.com/page/202'

res = requests.get(url, HEADERS)

try:
    res.raise_for_status()
except Exception as exc:
    print('Wrong!')

soup = BeautifulSoup(res.text, 'lxml')
items = soup.select('.entry_content>p>img')

for item in items:
    if not item:
        continue
    else:
        image = item.get('src')
        print(item)
        print(image)




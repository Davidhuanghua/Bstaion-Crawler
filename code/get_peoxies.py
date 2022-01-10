import re
import requests
from bs4 import BeautifulSoup


headers = {
    "Cache-Control": "max-age=2592000",
    "Content-Encoding": "gzip",
    "Content-Type": "text/css",
    "Date":"Thu, 25 Mar 2021 03:20:09 GMT",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

res = requests.get('https://www.kuaidaili.com/free/intr/', headers=headers, timeout=5)

if res.status_code == 200:
    data = BeautifulSoup(res.text, 'lxml')
    ip = data.find_all("td", {"data-title":"IP"})
    port = data.find_all("td", {"data-title":"PORT"})

    for i, j in zip(ip, port):
        a = re.findall('>(.*)<', str(i))
        b = re.findall('>(.*)<', str(j))
        with open('ip.txt', 'a', encoding='utf-8')as f:
            f.write(a[0])
            f.write(':'+b[0]+'\n')

        print(a[0], b[0])

else:
    print(res.status_code)
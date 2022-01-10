import requests

headers = {
    "Cache-Control": "max-age=2592000",
    "Content-Encoding": "gzip",
    "Content-Type": "text/css",
    "Date":"Thu, 25 Mar 2021 03:20:09 GMT",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

while True:
    p = {}
    with open('ip.txt', 'r')as f:
        all = f.readlines()
        for i in all:
            p['http'] = i.split('\n')[0]
            p['https'] = i.split('\n')[0]

            try:
                res = requests.get('https://www.baidu.com', proxies=p, headers=headers, timeout=5)
                if res.status_code == 200:
                    with open('ip_n.txt', 'a', encoding='utf-8')as f:
                        f.write(i)
                else:
                    pass
            except Exception as e:
                print(e)
    print('清洗完成')
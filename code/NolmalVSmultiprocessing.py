import os
import pymysql
import requests
import time
from multiprocessing import Pool


class Bili:
    # 定义变量
    def __init__(self):
        self.sql_1 = 'INSERT INTO userinfo(mid, follower, following) values(%s,%s,%s)'
        self.sql_2 = 'INSERT INTO userdata(mid, name, sex, sign, level, birthday, coins, ' \
                     'face_url, liveStatus, livingurl) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Origin': 'https://space.bilibili.com',
            'Connection': 'keep-alive',
            'Referer': 'https://space.bilibili.com/546195/fans/fans',
            'Cache-Control': 'max-age=0',
        }
        self.cookie = {'domain': '/',
                       'expires': 'false',
                       'httpOnly': 'false',
                       'name': 'buvid3',
                       'path': 'Fri, 29 Jan 2021 08:50:10 GMT',
                       'value': '7A29BBDE-VA94D-4F66-QC63-D9CB8568D84331045infoc,bilibili.com'}

    # 获取用户信息
    def get_info(self, url, mid):
        html = requests.get(url, headers=self.headers, cookies=self.cookie).json()['data']
        follower = html['follower']
        following = html['following']
        print("粉丝数：{}，关注数：{}".format(follower, following))
        print("-" * 50)
        with open('bili.log', 'a') as f2:
            f2.write('\n')
            f2.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'get_info: sucess!')

        db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='bilibili')
        cursor = db.cursor()
        try:
            cursor.execute(self.sql_1, (mid, follower, following))
            db.commit()
            with open('bili.log', 'a') as f2:
                f2.write('\n')
                f2.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'inserUserinfo: sucess!')
        except Exception as e:
            db.rollback()
            with open('error.log', 'a') as f:
                f.write('\n')
                f.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'userinfoInsertsql：%s' % str(e))
        db.close()

    # 获取头像
    def download_face(self, face_url, name):
        try:
            image = requests.get(face_url, headers=self.headers, cookies=self.cookie).content
            with open("../img/{}.jpg".format(name), 'wb') as f:
                f.write(image)
            with open('bili.log', 'a') as f2:
                f2.write('\n')
                f2.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'download_face: sucess!')
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write('\n')
                f.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'download_face: %s' % str(e))

    # 获取用户数据
    def get_userdata(self, url):
        try:
            html = requests.get(url, headers=self.headers, cookies=self.cookie, timeout=10)
            if html.status_code == 200:
                jsondata = html.json()['data']
                name = jsondata['name']
                sex = jsondata['sex']
                sign = jsondata['sign']
                level = jsondata['level']
                birthday = jsondata['birthday']
                coins = jsondata['coins']
                # 下载用户头像
                face_url = jsondata['face']
                self.download_face(face_url, name)
                # 获取直播间信息
                living = jsondata['live_room']
                roomStatus = living['roomStatus']
                liveStatus = living['liveStatus']
                livingurl = living['url']
                print('-' * 100)
                print("名字：{}  性别：{}  签名：{} 等级：{}  生日：{}  "
                      "硬币数目：{} 头像：{} \n 直播间状态：{} 直播间地址：{}".format(name, sex, sign, level, birthday, coins, face_url,
                                                                  liveStatus, livingurl))
                print('-' * 100)
                with open('bili.log', 'a') as f:
                    f.write('\n')
                    f.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'get_userdata: sucess!')
                return name, sex, sign, level, birthday, coins, face_url, liveStatus, livingurl
            else:
                print('网络连接错误，错误码：', html.status_code)
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write('\n')
                f.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'get_userdata: %s' % str(e))

    # 插入用户数据
    def insertUserdata(self, *args):
        db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='bilibili')
        cursor = db.cursor()
        try:
            cursor.execute(self.sql_2, args[0])
            db.commit()

        except Exception as e:
            db.rollback()
            with open('error.log', 'a') as f:
                f.write('\n')
                f.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'inseruserdata: %s' % str(e))
        db.close()

        with open('bili.log', 'a') as f:
            f.write('\n')
            f.write(time.strftime("%Y-%m-%d-%H:%M:%S ") + 'inseruserdata: sucess!')


def Start(mid_1, mid_2):
    print("进程{}开始".format(os.getpid()))
    bili = Bili()
    for i in range(mid_1, mid_2):
        # 获取userdata
        url1 = "https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp".format(i)
        # 获取userinfo
        url2 = "https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(i)

        try:
            bili.get_info(url2, i)
            time.sleep(5)
            userdata = bili.get_userdata(url1)
            args = list(userdata)
            args.insert(0, i)

            bili.insertUserdata(args)
            time.sleep(5)
            with open('error.log', 'a') as f:
                f.write('\n')
                f.write(time.strftime("%Y-%m-%d-%H:%M:%S") + 'Start: sucess!')
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write('\n')
                f.write('Start: %s' % str(e))
        finally:
            print("进程{}结束".format(os.getpid()))


if __name__ == '__main__':
    print('-' * 100)
    print('多进程爬虫与普通爬虫的爬取速度对比实验')
    print('-' * 100)
    print('-' * 100)

    print(10*'-', '《多进程爬虫》', 10*'-')
    print('-' * 100)
    start = time.time()
    p = Pool(5)
    # 爬取前20名用户数据，可修改为7亿内任何数字
    num = 5
    for mid_1, mid_2 in zip(range(1, num), range(2, num+1)):
        p.apply_async(Start, (mid_1, mid_2))

    # 关闭进程池，关闭后po不再接收新的请求
    p.close()
    p.join()

    print('程序运行结束！')
    end = time.time()
    print('-' * 100)
    print('多进程爬虫运行时间：', end-start)

    # 普通爬虫
    print('-' * 100)
    print(10 * '-', '《普通爬虫》', 10 * '-')
    print('-' * 100)
    start = time.time()
    Start(1, 5)
    end = time.time()
    print('-' * 100)
    print('普通爬虫运行时间：', end - start)
    print('-' * 100)
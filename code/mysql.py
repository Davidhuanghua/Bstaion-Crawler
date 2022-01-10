# 数据库设计
import pymysql


class Creater:

    def __init__(self):
        self.sql_0 = 'DROP DATABASE bilibili;'

        self.sql_1 = 'CREATE DATABASE bilibili;'

        self.sql_2 = '''CREATE TABLE IF NOT EXISTS `userinfo`(
                     `mid` int(11) NOT NULL AUTO_INCREMENT,
                     `follower` VARCHAR(255),
                     `following` VARCHAR(255),
                        PRIMARY KEY (mid));'''

        self.sql_3 = 'CREATE TABLE IF NOT EXISTS userdata (' \
                     'mid int(11) NOT NULL AUTO_INCREMENT,' \
                     'name VARCHAR(255),' \
                     'sex VARCHAR(255),' \
                     'sign VARCHAR(255) , ' \
                     'level VARCHAR(255),' \
                     'birthday VARCHAR(255),' \
                     'coins VARCHAR(255),' \
                     'face_url VARCHAR(255),' \
                     'liveStatus VARCHAR(255),'\
                     'livingurl VARCHAR(255),' \
                     'PRIMARY KEY (mid))'

        self.cha = 'select * from userinfo;'

    def chaxun(self):
        db = pymysql.connect(host="localhost", user="root", password="root", database="bilibili")
        cursor = db.cursor()
        cursor.execute(self.cha)
        get_row = cursor.fetchall()
        print(get_row)
        cursor.close()
        db.close()

    def insert_test(self, *args):
        # 写入数据库
        insert = 'INSERT INTO bilibili_user_info(id, mid, name, sex, following, fans, level) ' \
                 'VALUES (1,2,3,4,5,6,7)'

        # 数据库账号，密码，数据库名
        db = pymysql.connect(host="localhost", user="root", password="root", database="bilibili")
        cursor = db.cursor()
        cursor.execute(insert)

        db.commit()
        db.close()

    def createdb(self):

        # 建库(1)
        db = pymysql.connect(host='localhost', user='root', password='root', port=3306)
        cursor_1 = db.cursor()
        cursor_1.execute(self.sql_0)
        cursor_1.execute(self.sql_1)
        cursor_1.close()
        # 建表
        db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='bilibili')
        cursor_2 = db.cursor()
        cursor_2.execute(self.sql_2)

        cursor_3 = db.cursor()
        cursor_3.execute(self.sql_3)
        db.close()


if __name__ == '__main__':
    do = Creater()
    # do.insert_test()
    # do.chaxun()
    do.createdb()
    print('完成')
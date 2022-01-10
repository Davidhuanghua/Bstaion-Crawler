# 数据可视化（男女比例）
from pyecharts import Pie
# pip install pyecharts==0.1.9.4
import pymysql


db = pymysql.connect(host="localhost", user="root", password="root", database="bilibili")
cursor = db.cursor()
cursor.execute('select sex from userdata;')
get_row = cursor.fetchall()

boy = 0
girl = 0
unknow = 0
for i in get_row:
    sex = i[0]
    if sex == '男':
        boy += 1
    elif sex == '女':
        girl += 1
    elif sex == '保密':
        unknow += 1
print('男：',boy,'\n','女：',girl,'\n','保密：',unknow)

attr = ["男生", "女生", "保密"]
v1 = [boy, girl, unknow]
pie = Pie("B站用户男女比例饼状图")
pie.add("", attr, v1, is_label_show=True)
pie.render()




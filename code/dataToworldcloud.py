import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba


def get():
    db = pymysql.connect(host="localhost", user="root", password="root", database="bilibili")
    cursor = db.cursor()
    cursor.execute('select sign,name from userdata;')
    get_row = cursor.fetchall()

    for i in get_row:
        if len(i[0]) == 0:
            pass
        else:
            with open('sign.txt', 'a', encoding='utf-8')as f:
                print(i[0])
                f.write(i[0])
    cursor.close()
    db.close()


def tocloud():
    path_txt = 'sign.txt'
    f = open(path_txt, 'r', encoding='UTF-8').read()

    cut_text = " ".join(jieba.cut(f))

    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/simfang.ttf",
        background_color="black",
        width=1000,
        height=880).generate(cut_text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('worldcloud.png')
    plt.show()

try:
    get()
    tocloud()
except Exception as e:
    print(e)

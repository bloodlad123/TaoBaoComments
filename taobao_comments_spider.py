import requests
from fake_useragent import UserAgent
import json
import os
import time
import jieba
import random
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

tao_bao_comments = 'D:/Python/practise_file/tb_comments.txt'


def cut_word():  # 对数据分词
    with open(tao_bao_comments, encoding='utf-8') as f:
        content_txt = f.read()
        word_list = jieba.cut(content_txt, cut_all=True)
        wl = ' '.join(word_list)
        print(wl)
    return wl


# def create_word_cloud():  # 生成词云
#     wc = WordCloud(font_path='C:/Windows/Fonts/SIMLI.TTF', background_color='white', width=1000,
#     height=880)  # 设置词云的一些配置
#     word_cloud = wc.generate(cut_word())  # 生成词云
#     word_cloud.to_file('word_cloud.jpg')    # 保存图片
#     plt.imshow(word_cloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.show()
# def create_word_cloud():  # 生成词云
#     background_image = np.array(Image.open('wristband.jpg'))  # 设置词云形状图片
#     wc = WordCloud(font_path='C:/Windows/Fonts/SIMLI.TTF',   # 设置字体为本地的字体，有中文必须要加
#                    background_color='white',    # 设置背景的颜色，需与背景图片的颜色保持一致，否则词云的形状会有问题
#                    scale=4,
#                    max_words=100,     # 设置最大的字数
#                    max_font_size=100,   # 设置字体的最大值
#                    random_state=40,     # 设置有多少种随机生成状态，即有多少种配色方案
#                    mask=background_image)  # 设置词云的一些配置,有mask参数再设定宽高是无效的
#     wc.generate_from_text(cut_word())  # 生成词云
#     wc.to_file('wc.jpg')    # 保存图片
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis('off')  # 不显示坐标轴
#     plt.show()

def create_word_cloud():  # 生成词云
    background_image = np.array(Image.open('wristband.jpg'))  # 设置词云形状图片
    image_colors = ImageColorGenerator(background_image)
    # 生成词云
    wc = WordCloud(font_path='C:/Windows/Fonts/SIMLI.TTF',   # 设置字体为本地的字体，有中文必须要加
                   background_color='white',    # 设置背景的颜色，需与背景图片的颜色保持一致，否则词云的形状会有问题
                   scale=4,
                   max_words=100,     # 设置最大的字数
                   max_font_size=100,   # 设置字体的最大值
                   random_state=40,     # 设置有多少种随机生成状态，即有多少种配色方案
                   mask=background_image,
                   color_func=image_colors).generate_from_text(cut_word())  # 设置词云的一些配置,有mask参数再设定宽高是无效的
    wc.to_file('wc.jpg')  # 保存图片
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.show()


def comment_save(res_json_comments):
    for res_json_comment in res_json_comments:
        comment = res_json_comment['rateContent']
        # print(comment + '\n')
        with open(tao_bao_comments, 'a+', encoding='utf-8') as f:
            f.write(comment + '\n')


def comment_spider(page):   
    ua = UserAgent()
    header = {'UserAgent': ua.random, 'Referer': 'https://detail.tmall.com/item.htm?spm=a230r.1.14.6.3541328a4ewHF6 \
                &id=577994735177&cm_id=140105335569ed55e27b&abbucket=6', 'Cookie': 'cna=B9MzEZcW6hoCAcp53x4nJXWV; hng \
                =CN%7Czh-CN%7CCNY%7C156; dnk=idiotes; uc1=pas=0&tag=8&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&coo \
                kie14=UoTaHPrQxAtVJw%3D%3D&lng=zh_CN&existShop=true&cookie15=UIHiLt3xD8xYTw%3D%3D&cookie21=VFC%2FuZ9 \
                ajCbF99I65Qm9gQ%3D%3D; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=CsLp%2FX%2FPPg%3D%3D&id2=UUtJZPuNBUfoQg% \
                3D%3D&vt3=F8dBy3zVzCJd36GCj5Y%3D; tracknick=idiotes; lid=idiotes; _l_g_=Ug%3D%3D; unb=2323732055; lg \
                c=idiotes; cookie1=Vq1DmrfZtY%2FxxB7hOJOizQD3xao1UueTu27ST12UuRY%3D; login=true; cookie17=UUtJZPuNBU \
                foQg%3D%3D; cookie2=106d63c4228084db6f8cb0e82e7bb64c; _nk_=idiotes; sg=s5e; t=4586f90f6a57afcf89ef89 \
                8b1134c8f5; csg=120d3305; enc=e6X%2FK4c6EBRvF5tSSctk670hdG8eYybHrxf6X12S5noD95fFdwjA0X8gZ8K6w5xsVJ0d \
                YtarIAgvcr5YVa9Y1Q%3D%3D; _tb_token_=3e45763558e83; l=cBxHgk7eqOJTNC2vBOfwZuI8Ld7t1IObzxVzw4OGuICPOr \
                1XXRk1WZ3IWa8WCnhVL6kpJ3WHB0HYBlLEGPathZXRFJXn9MpO.; isg=BHp6goVz88ilJH-cowcAz6x5y6Bcg_90kuhhVoRyQo2 \
                JdxixbbrZFyfBxkMOVXad'}
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=577994735177&spuId=1209316247&sellerId=2616970884&order \
            =3&currentPage=%s' % page
    res = requests.get(url, headers=header)
    # 截取json数据字符串
    res_json_str = res.text[11:-1]
    # 字符串转json对象
    # print(res_json_str)
    res_json_obj = json.loads(res_json_str)
    # 获取评价列表数据
    res_json_comments = res_json_obj['rateDetail']['rateList']
    # print(type(res_json_comments)) # list
    comment_save(res_json_comments)


def main():
    # 判断括号里的文件是否存在,存在则清除
    if os.path.exists(tao_bao_comments):
        os.remove(tao_bao_comments)
    for page in range(1, 11):
        comment_spider(page)
        time.sleep(random.random()*5)
    create_word_cloud()


if __name__ == '__main__':
    main()
# print(res.raise_for_status())



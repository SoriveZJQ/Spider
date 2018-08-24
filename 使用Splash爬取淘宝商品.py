#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import requests
import pymongo
from urllib.parse import quote
from pyquery import PyQuery as pq


BASE_URL = 'https://s.taobao.com/search?q='
KEYWORD = 'iPad'
MAX_PAGE = 5
MONGO_URI = 'localhost'
MONGO_DB = 'taobao_2'
COLLECTION = 'products'


def get_one_page(page):
    print('正在爬取第' + str(page) + '页')
    url = BASE_URL + quote(KEYWORD)
    lua = '''
    function main(splash, args)
        splash:go(args.url)
        splash:wait(3)
        input = splash:select(".input.J_Input")
        input:send_keys("<Delete>")
        input:send_keys("<Backspace>")
        input:send_text(args.page)
        submit = splash:select(".btn.J_Submit")
        submit:mouse_click()
        splash:wait(3)
        return splash:html()
    end
    '''
    url = 'http://192.168.99.100:8050/execute?lua_source=' + quote(lua) + '&url=' + url + '&page=' + str(page)
    response = requests.get(url)
    return response.text


i = 1


def parse_one_page(html):
    global i
    i = 1
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        save_to_mongo(product)


client = pymongo.MongoClient()
db = client[MONGO_DB]


def save_to_mongo(product):
    global i
    try:
        if db[COLLECTION].insert(dict(product)):
            print('{}号商品存储到MongoDB成功！'.format(i))
            i += 1
    except Exception:
        print('{}号商品存储到MongoDB失败！'.format(i))
        i += 1


if __name__ == '__main__':
    for page in range(1, MAX_PAGE + 1):
        html = get_one_page(page)
        parse_one_page(html)

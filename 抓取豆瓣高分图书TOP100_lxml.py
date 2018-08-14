#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import requests
from requests.exceptions import RequestException
import time
from lxml import etree
import json


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    html = etree.HTML(html)
    titles = html.xpath('//div[@class="title"]/a/text()')
    if len(titles) < 25:
        images = html.xpath('//div[@class="post"]/a/img/@src')
        addresses = html.xpath('//div[@class="post"]/a/@href')
        information = html.xpath('//div[@class="abstract"]/text()')
        scores = html.xpath('//span[@class="rating_nums"]/text()')
        numbers = html.xpath('//div[@class="rating"]/span[3]/text()')

        for i in range(24):
            yield {
                'title': titles[i].strip(),
                'image': images[i],
                'address': addresses[i],
                'author': information[3 * i].strip()[3:] if len(information[3 * i]) > 3 else '',
                'publisher': information[3 * i + 1].strip()[4:] if len(information[3 * i + 1]) > 4 else '',
                'time': information[3 * i + 2].strip()[4:] if len(information[3 * i + 2]) > 4 else '',
                'score': scores[i],
                'number': numbers[i]
            }
    else:
        images = html.xpath('//div[@class="post"]/a/img/@src')
        addresses = html.xpath('//div[@class="post"]/a/@href')
        information = html.xpath('//div[@class="abstract"]/text()')
        if len(information) < 75:
            information.insert(69, '作者：无')
        scores = html.xpath('//span[@class="rating_nums"]/text()')
        numbers = html.xpath('//div[@class="rating"]/span[3]/text()')

        for i in range(25):
            yield {
                'title': titles[i].strip(),
                'image': images[i],
                'address': addresses[i],
                'author': information[3 * i].strip()[3:] if len(information[3 * i]) > 3 else '',
                'publisher': information[3 * i + 1].strip()[4:] if len(information[3 * i + 1]) > 4 else '',
                'time': information[3 * i + 2].strip()[4:] if len(information[3 * i + 2]) > 4 else '',
                'score': scores[i],
                'number': numbers[i]
            }


def write_to_file(content):
    with open('DoubanResult_lxml', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(start):
    url = 'https://www.douban.com/doulist/45004834/?start=' + str(start) + '&sort=time&sub_type='
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(4):
        main(start=i * 25)
        time.sleep(1)

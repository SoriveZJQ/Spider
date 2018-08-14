#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import requests
from requests.exceptions import RequestException
import re
import time
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
    pattern = re.compile(
        'class="source".*?class="post">.*?<img.*?src="(.*?)".*?class="title".*?href="(.*?)".*?>(.*?)</a>.*?class='
        '"rating_nums">(.*?)</span>.*?<span>(.*?)</span>.*?class="abstract">(.*?)<br />(.*?)<br />(.*?)</ div>', re.S
    )

    items = re.findall(pattern, html)

    for item in items:
        yield {
            'title': items[2].strip(),
            'image': item[0].strip(),
            'address': item[1].strip(),
            'author': item[5].strip()[3] if len(item[5]) > 3 else '',
            'publisher': item[6].strip()[4] if len(item[6]) > 4 else '',
            'time': item[7].strip()[4] if len(item[7]) > 4 else '',
            'score': item[3].strip(),
            'number': item[4].strip()
        }


def write_to_file(content):
    with open('DoubanResult_正则.txt', 'a', encoding='utf-8') as fp:
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

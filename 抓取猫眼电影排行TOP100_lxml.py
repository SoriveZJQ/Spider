#!/usr/bin/env python 
# -*- coding:utf-8 -*-


from lxml import etree
import requests
import json
from requests.exceptions import RequestException
import time


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
    resultindexs = html.xpath('//dd/i[contains(@class, "board-index")]/text()')
    resultimages = html.xpath('//dd/a/img/@data-src')
    resulttitles = html.xpath('//dd/div/div/div/p[@class="name"]/a/text()')
    resultactors = html.xpath('//dd/div/div/div/p[@class="star"]/text()')
    resulttimes = html.xpath('//dd/div/div/div/p[@class="releasetime"]/text()')
    resultscores = html.xpath('//dd/div/div/div/p[@class="score"]/i/text()')
    for i in range(10):
        yield {
            'index': resultindexs[i],
            'image': resultimages[i],
            'title': resulttitles[i].strip(),
            'actor': resultactors[i].strip()[3:],
            'time': resulttimes[i].strip()[5:],
            'score': (resultscores[2*i]+resultscores[2*i+1]).strip()
        }


def write_to_file(content):
    with open('result_lxml.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
        time.sleep(1)

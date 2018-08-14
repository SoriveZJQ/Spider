#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import requests
import time
import json
from requests.exceptions import RequestException
from pyquery import PyQuery as pq


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return  None
    except RequestException:
        return None


def parse_one_page(html):
    doc = pq(html)
    indexs = doc('.board-index').text().split()
    images = []
    for item in doc('.board-img').items():
        images.append(item.attr('data-src'))
    titles = doc('.name').text().split()
    actors = doc('.star').text().split()
    times = doc('.releasetime').text().split()
    scores = doc('.score').text().split()

    for i in range(10):
        yield {
            'index': indexs[i],
            'image': images[i],
            'title': titles[i],
            'actor': actors[i].strip()[3:] if len(actors[i]) > 3 else '',
            'time': times[i].strip()[5:] if len(times[i]) > 5 else '',
            'score': scores[i]
        }


def write_to_file(content):
    with open('result_pyquery.txt', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)

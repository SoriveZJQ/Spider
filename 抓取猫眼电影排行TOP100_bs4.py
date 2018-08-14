#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import json
import time
import requests
from requests import exceptions
from bs4 import BeautifulSoup


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except exceptions.RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    indexsAndScores = []
    for i in range(30):
        indexsAndScores.append(soup.select('dd i')[i].get_text())
    images = []
    for i in range(10):
        images.append(soup.find_all(class_='board-img')[i].attrs['data-src'])
    titles = []
    for i in range(10):
        titles.append(soup.find_all(class_='name')[i].string)
    actors = []
    for i in range(10):
        actors.append(soup.find_all(class_='star')[i].string)
    times = []
    for i in range(10):
        times.append(soup.find_all(class_='releasetime')[i].string)
    for i in range(10):
        yield {
            'index': indexsAndScores[i*3],
            'image': images[i],
            'title': titles[i].strip(),
            'actor': actors[i].strip()[3:] if len(actors[i]) > 3 else '',
            'time': times[i].strip()[5:] if len(times[i]) > 5 else '',
            'score': (indexsAndScores[3*i+1] + indexsAndScores[3*i+2]).strip()
        }


def write_to_file(content):
    with open('result_bs4.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)

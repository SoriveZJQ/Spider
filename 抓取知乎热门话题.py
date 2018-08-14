#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq


def main(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/65.0.3325.162 Safari/537.36'
        }

        html = requests.get(url, headers=headers).text
        doc = pq(html)
        items = doc('.explore-tab .feed-item').items()
        for item in items:
            question = item.find('h2').text()
            author = item.find('.author-link').text()
            answer = pq(item.find('.content').html()).text()
            with open('explore.txt', 'a', encoding='utf-8') as fp:
                fp.write('\n'.join([question, author, answer]))
                fp.write('\n' + '='*50 + '\n')
    except RequestException:
        return None


if __name__ == '__main__':
    url = 'https://www.zhihu.com/explore'
    main(url)

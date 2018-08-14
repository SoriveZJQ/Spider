#!/usr/bin/env python
# -*- coding:utf-8 -*-


from selenium import webdriver
import json


def parse_page(url):
    browser = webdriver.Chrome()
    browser.get(url)
    browser.switch_to.frame('contentFrame')
    ranks = []
    nodes = browser.find_elements_by_css_selector('span.num')
    for node in nodes:
        ranks.append(node.text)
    names = []
    nodes = browser.find_elements_by_css_selector('.ttc .txt b')
    for node in nodes:
        names.append(node.get_attribute('title'))
    singers = []
    nodes = browser.find_elements_by_css_selector('div.text')
    for node in nodes:
        singers.append(node.get_attribute('title'))
    songs = []
    nodes = browser.find_elements_by_css_selector('span.txt a')
    for node in nodes:
        songs.append(node.get_attribute('href'))
    for i in range(100):
        yield {
            'index': ranks[i],
            'song': names[i],
            'singer': singers[i],
            'url': songs[i]
        }


def write_to_file(content):
    with open('网易云音乐新歌TOP100.txt', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    url = 'https://music.163.com/#/discover/toplist?id=3779629'
    for item in parse_page(url):
        print(item)
        write_to_file(item)

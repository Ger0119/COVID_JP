#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/01/27 16:55
# @Author  : Ketsu Kin
# @File    : Downloader.py
import re
import json
import requests
from lxml import etree
from datetime import datetime
from fake_useragent import UserAgent


def download(target="都道府県ごとの感染者数", base="https://www3.nhk.or.jp/"):
    menu = "/news/special/coronavirus/"
    pat_navi = re.compile(r'<script>\s*writeInclude\("(.*?)"\);')
    pat_urls = re.compile(r'<a href="(?P<url>.*?)".*?<span>(?P<title>.*?)</span>')
    pat_json = re.compile(r'lab.JsonGetter\("(.*?)"')
    pat_csv = re.compile(r'<opendata>(.*?)</opendata>')

    # base から URLを抽出　　　https://www3.nhk.or.jp/news/special/coronavirus/module/mod_navi.html
    url_navi = base[:-1] + get_url(base + menu, pat_navi)
    # Data フォルダに url.csvを作成
    get_urls(url_navi, pat_urls, base)
    # url.csvから targetのURLを抽出してdata URLを抽出　　https://www3.nhk.or.jp/news/special/coronavirus/data/　
    url_data = get_target_url(target)
    # data URLから json URLを抽出　　　 https://www3.nhk.or.jp/news/special/coronavirus/data/conf_widget.json
    url_json = base[:-1] + get_json(url_data, pat_json)
    # json URLから xml URLを抽出
    url_xml = base[:-1] + get_xml(url_json)
    # xml URLから csv URLを抽出
    url_csv = [base[:-1] + x for x in get_csv(url_xml, pat_csv)]
    # csv をdownloadする
    download_csv(url_csv)


def request(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    if res.status_code != 200:
        print(f"Access Website Error: {url}")
        return None
    data = res.text
    res.close()

    return data


def get_url(url, pat):
    res = request(url)
    return pat.findall(res)[2]


def get_urls(url, pat, base):
    res = request(url)
    data = pat.findall(res)
    with open("Data/url.csv", "w+") as f:
        for (x, y) in data:
            f.write(f'{y},{base[:-1]}{x},\n')


def get_target_url(target):
    url = ""
    with open("Data/url.csv") as f:
        for x in f.readlines():
            data = x.split(',')
            if data[0] == target:
                url = data[1]
                break
    return url


def get_json(url, pat):
    res = request(url)
    tree = etree.HTML(res)
    return pat.findall(tree.xpath('//*[@id="index"]/script[6]/text()')[0])[0]


def get_xml(url):
    res = request(url)
    return json.loads(res)["xmlPath"]


def get_csv(url, pat):
    res = request(url)
    return list(set(pat.findall(res)))


def download_csv(lst):
    for csv in lst:
        name = csv.split('/')[-1]
        with open(f"Data/{name}", "w+", encoding='utf-8') as f:
            f.write(request(csv))
        print(f"{name} download over!")

    with open("Data/download_time.log", "w+") as f:
        f.write(str(datetime.now()))


if __name__ == "__main__":
    download()

# -*- coding: utf-8 -*-
import scrapy
import json
import pymongo
from newsqq.items import NewsqqItem


class LinksSpiderSpider(scrapy.Spider):
    name = 'phone_list'

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.newsQQDB = self.client['newsQQDB']
        self.newparam = self.newsQQDB['newparam']
        # 生成需要爬取的链接
        self.alllink = []
        result = self.newparam.find_one({'splider_name': 'phone_list'})
        pagelinks = result['page_links']
        token = result['token']
        limit_page = result['limit_page']
        for page in range(1, limit_page + 1):
            num = 0  # 第一个类型
            for link in pagelinks:
                next_page = link.split('，')[2].format(token, str(page))
                next_str = link.split('，')[0] + "，" + link.split('，')[1] + "，" + next_page
                self.alllink.append(next_str)
                num += 1  # 下一个类型
        self.num = 0
        self.limit_num = len(self.alllink)
        s_url = self.alllink[self.num].split('，')[2]
        self.start_urls = [s_url]  # 入口链接
        print(s_url)

    def parse(self, response):
        print('爬虫phone_list的目标链接开始爬取...')
        print(response.request.headers['User-Agent'])
        news_data = json.loads(response.text)
        item_list = news_data['data']
        print(len(item_list))
        news = NewsqqItem()
        for item in item_list:
            news['category'] = self.alllink[self.num].split('，')[0]
            news['cate_en'] = self.alllink[self.num].split('，')[1]
            news['title'] = item['title']
            news['href'] = item['vurl']
            news['image'] = item['img']
            news['article'] = 'none'
            news['introduce'] = item['intro']
            news['keywords'] = item['keywords']
            news['time'] = item['publish_time']
            news['source'] = item['source']
            news['istoexcel'] = 0
            yield news
        self.num += 1
        if self.num < self.limit_num:
            print(self.num)
            next_link = self.alllink[self.num].split('，')[2]
            print(next_link)
            yield scrapy.Request(next_link, callback=self.parse)

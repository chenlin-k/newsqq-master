# -*- coding: utf-8 -*-
import scrapy
import pymongo
from newsqq.items import NewsqqItem


class TxNewsContentByPcSpider(scrapy.Spider):
    name = 'pcContent_spider'

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.newsQQDB = self.client['newsQQDB']
        self.links = self.newsQQDB['pclinks']
        self.article = self.newsQQDB['article']
        links_array = [i['href'] for i in self.links.find()]
        article_array = [i['href'] for i in self.article.find()]
        x = set(links_array)
        y = set(article_array)
        print('总共需获取' + str(len(x)), '已获取' + str(len(y)))
        left_set = x.difference(y)
        self.myLinks = list(left_set)
        self.myNum = 0
        self.myLimit = len(left_set)
        print('此次需要获取的正文数为' + str(self.myLimit) + '，开始获取链接正文...')
        self.allowed_domains = ['new.qq.com']
        if self.myLimit==0:
            s_url = 'http://new.qq.com'
        else:
            s_url = self.myLinks[0]
        self.start_urls = [s_url]

    def parse(self, response):
        print('爬虫pcContent_spider的目标链接开始爬取...')
        if response.url =='https://new.qq.com/':
            print('此次爬虫没有需要获取的正文！')
        else:
            try:
                href = response.meta.get('href', '')
                article_item = NewsqqItem()
                title = response.xpath('/html/head/title/text()').extract()[0]
                contents = response.xpath('//*[@class="content-article"]/p/text()').extract()
                content = "\n".join(contents)
                create_date = response.xpath('/html/head/meta[3]/@content').extract_first()
                # if not content.strip() :
                url = response.url
                article_item['href'] = url
                article_item['title'] = title
                article_item['article'] = content
                article_item['platform']='PC'
                yield article_item
                self.links.update({'href': self.myLinks[self.myNum]},
                                  {'$set': {'time': create_date, 'title': title, 'status': 1}})
            except Exception as e:
                print('链接解析出现异常...')
            self.myNum += 1
            if self.myNum < self.myLimit:
                print(self.myNum)
                next_link = self.myLinks[self.myNum]
                print(next_link)
                yield scrapy.Request(next_link, callback=self.parse)


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class NewsqqPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.newsQQDB = self.client['newsQQDB']
        self.pclinks=self.newsQQDB['pclinks']
        self.links = self.newsQQDB['links']
        self.article = self.newsQQDB['article']

    def process_item(self, item, spider):
        if spider.name == 'phone_list':
            data = dict(item)
            count = self.links.find({'href': item['href']}).count()
            if count == 0:
                self.links.insert(data)
            return item
        elif spider.name == 'pc_list':
            data2 = dict(item)
            #若爬虫的效率比较低，则可把这行去除达到优化的效果
            count = self.pclinks.find({'href': item['href']}).count()
            if count == 0:
                self.pclinks.insert(data2)
            return item
        elif spider.name == 'pcContent_spider':
            data3 = dict(item)
            count = self.article.find({'href': item['href']}).count()
            if count == 0:
                self.article.insert(data3)
            return item
        elif spider.name == 'phoneContent_spider':
            data3 = dict(item)
            count = self.article.find({'href': item['href']}).count()
            if count == 0:
                self.article.insert(data3)
            return item
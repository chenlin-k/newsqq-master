import re
import scrapy
import pymongo
from newsqq.items import NewsqqItem


# 爬取腾讯新闻电脑端的新闻页面内容
class TxNewsListByPcSpider(scrapy.Spider):
    name = 'pc_list'
    allowed_domains = ['qq.com']
    start_urls = ['http://www.qq.com/map/']

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.newsQQDB = self.client['newsQQDB']
        self.newparam = self.newsQQDB['newparam']
        self.pclinks = self.newsQQDB['pclinks']
        self.article = self.newsQQDB['article']
        result = self.newparam.find_one({'splider_name': 'pc_list'})
        self.start_urls=result['page_links']

    def parse(self, response):
        print('爬虫pc_list的目标链接开始爬取...')
        urls_list = []
        for i in response.xpath('//*[@id="wrapCon"]/div/div[1]/div[2]/dl[1]'):
            urls = i.xpath('dd/ul/li/strong/a/@href').extract() or i.xpath('dd/ul/li/a/@href').extract()
            urls_list.extend(i.strip() for i in urls)
        for url in urls_list:
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        pat = re.compile('http://new.qq.com/.*/.*.html')
        detail_urls = pat.findall(response.text)
        detail_urls = list(set(detail_urls))
        new_list = []
        for i in detail_urls:
            i = "https:" + i.split(':')[1]
            new_list.append(i)
        got_href = [i['href'] for i in self.pclinks.find()]
        x = set(new_list)
        y = set(got_href)
        diff_array = x.difference(y)
        link_item = NewsqqItem()
        if len(diff_array) > 0:
            for url in diff_array:
                if url:
                    link_item['href'] = url
                    link_item['status'] = 0  # 表示正文未进行采集
                    link_item['istoexcel'] = 0
                    link_item['article'] = 'none'
                    yield link_item
                    # self.pclinks.insert(dict(link_item))
                    # yield scrapy.Request(url=url, meta={'href': url}, callback=self.parse_url)
        else:
            print('已经爬取目标连接完毕~')

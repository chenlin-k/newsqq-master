import scrapy
import pymongo
from newsqq.items import NewsqqItem


class TxNewsContentByPhoneSpider(scrapy.Spider):
    name = 'phoneContent_spider'

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.newsQQDB = self.client['newsQQDB']
        self.links = self.newsQQDB['links']
        self.article = self.newsQQDB['article']
        print('正在更新数据库...')
        for i in self.links.find():  # 更新数据库，将http链接转为https
            new_href = "https:" + i['href'].split(':')[1]
            self.links.update_one({'href': i['href']}, {'$set': {'href': new_href}})
        print('更新完成')
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
        s_url = self.myLinks[0]
        self.start_urls = [s_url]

    def parse(self, response):
        print('爬虫phoneContent_spider的目标链接开始爬取...')
        try:
            news = NewsqqItem()
            article_array = []
            print(response.request.headers['User-Agent'])
            contents = response.xpath('//*[@class="content-article"]/p/text()').extract()
            content = "\n".join(contents)
            #获取正文内容
            # p_list = response.xpath("//p[1]//parent::div/p")
            # for p in p_list:
            #     p_str = p.xpath("./text()").extract_first()
            #     if p_str:
            #         article_array.append(p_str)
            # article_str = '\n'.join(article_array)
            news['article'] = content
            news['href'] = response.request.url
            news['platform'] = 'PHONE'
            yield news
        except Exception as e:
            print('xpath解析出现异常...')
        self.myNum += 1
        if self.myNum < self.myLimit:
            print(self.myNum)
            next_link = self.myLinks[self.myNum]
            print(next_link)
            yield scrapy.Request(next_link, callback=self.parse)

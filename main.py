import datetime
import time
import pymongo
import os


# 清空mongodb数据库中的数据
def deleteMongoDB():
    client = pymongo.MongoClient('localhost', 27017)
    newsQQDB = client['newsQQDB']
    links = newsQQDB['links']
    article = newsQQDB['article']
    pclinks = newsQQDB['pclinks']
    newparam = newsQQDB['newparam']
    links.remove()
    article.remove()
    pclinks.remove()
    newparam.remove()
    print('已清空数据库，开始运行程序')


if __name__ == '__main__':
    # 清空数据库
    # deleteMongoDB()

    while True:
        now_time = datetime.datetime.now()
        print(now_time)
        current_time = time.localtime(time.time())
        if ((current_time.tm_hour == 15) and (current_time.tm_min == 20) and (current_time.tm_sec == 30)):
            print('开始生成需获取的所有页面链接...')

            os.system('python autoGetlink.py')

            print('开始获取PC端所有页面的新闻链接...')
            os.system('scrapy crawl pc_list')  # 执行正文爬虫

            print('开始获取PHONE端所有页面的新闻链接...')
            os.system('scrapy crawl phone_list')

            print('开始获取PHONE端所有页面的正文内容...')
            os.system('scrapy crawl phoneContent_spider')

            print('开始获取PC端所有页面的正文内容...')
            os.system('scrapy crawl pcContent_spider')
            # print("Hello World1")
        if ((current_time.tm_hour == 11) and (current_time.tm_min == 30) and (current_time.tm_sec == 0)):
            print('所有新闻文章正文获取完毕！正在导出...')
            os.system('python linksAndArticleToExcel.py')
            print('已导出')
            # print("Hello World2")
        time.sleep(1)






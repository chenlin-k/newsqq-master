import pymongo
import pandas
import time
import os

client = pymongo.MongoClient('localhost', 27017)
newsQQDB = client['newsQQDB']
links = newsQQDB['links']
pclinks = newsQQDB['pclinks']
article = newsQQDB['article']

# 导出的excel文件的地址
export_pcurl = 'd:\\tencentNewsplider\pc\{}'.format(time.strftime("%m%d", time.localtime())) + '.xlsx'
export_phoneurl = 'd:\\tencentNewsplider\phone\{}'.format(time.strftime("%m%d", time.localtime())) + '.xlsx'


def phone_toexcel():
    for i in article.find({'platform': 'PHONE'}):
        links.update_one({'href': i['href']}, {'$set': {'article': i['article']}})
        links.update_one({'href': i['href']}, {'$set': {'article': i['article']}})

    for i in links.find().limit(1):
        if isinstance(i['keywords'], list):
            print('keywords已经是list')
        else:
            print('keywords正在转为list')
            for j in links.find():
                keywords_array = j['keywords'].split(';')
                links.update_one({'href': j['href']}, {'$set': {'keywords': keywords_array}})
    # links表放到Excel中
    array = [i for i in links.find({}, {'istoexcel': 0})]
    if len(array) > 0:
        df = pandas.DataFrame(array)
        try:
            df.to_excel(export_phoneurl)
        except Exception as e:
            print('导出PHONE端数据失败...')
            print(e)
        else:
            for i in links.find({'istoexcel': 0}):
                # 更新数据库，将未导出到excel改成已导出
                links.update_one({'href': i['href']}, {'$set': {'istoexcel': 1}})
    else:
        print('暂无PHONE端数据需要导出到excel中！')


def pc_toexcel():
    for i in article.find({'platform': 'PC'}):
        pclinks.update_one({'href': i['href']}, {'$set': {'article': i['article']}})
        pclinks.update_one({'href': i['href']}, {'$set': {'article': i['article']}})
    array = [i for i in pclinks.find({}, {'istoexcel': 0})]
    if len(array) > 0:
        df = pandas.DataFrame(array)
        try:
            df.to_excel(export_pcurl)
        except Exception as e:
            print('导出PC端数据失败...')
            print(e)
        else:
            for i in pclinks.find({'istoexcel': 0}):
                # 更新数据库，将未导出到excel改成已导出
                pclinks.update_one({'href': i['href']}, {'$set': {'istoexcel': 1}})
    else:
        print('暂无PC端数据需要导出到excel中！')


phone_toexcel()
pc_toexcel()

# command = 'mongoexport -d newsQQDB -c links --type=json -o ./data/{}.json'.format(name)
# os.system(command)

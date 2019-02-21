import pymongo
import time
import random

client = pymongo.MongoClient('localhost', 27017)

newsQQDB = client['newsQQDB']
newparam=newsQQDB['newparam']


#生成爬取Phone端新闻类型的参数
def productPhonelistLink():
    param={}
    param['source']='qqnews'
    param['status']=0 #0(开启采集) 1(采集完毕)
    param['token']='c232b098ee7611faeffc46409e836360' #token值
    param['splider_name']='phone_list'
    param['limit_page']=10 #爬取的页码
    type_links=[]
    with open('type_links.txt', 'rt', encoding='UTF-8') as f:
        for line in f:
            type_links.append(line.strip())
    param['page_links']=type_links
    data=dict(param)
    count = newparam.find({'splider_name': 'phone_list'}).count()
    if count == 0:
        newparam.insert(data)

# 生成爬取Pc端新闻类型的参数
def productPclistLink():
    param={}
    param['source']='qqnews'
    param['status']=0 #0(开启采集) 1(采集完毕)
    param['token'] = '无需token'  # token值
    param['splider_name']='pc_list'
    param['limit_page']=0 #爬取的页码
    type_links=['http://www.qq.com/map/']
    param['page_links']=type_links
    data=dict(param)
    count = newparam.find({'splider_name': 'pc_list'}).count()
    if count == 0:
        newparam.insert(data)

#--------------------------------------
print('PC端新闻类型的参数开始生产...')
productPhonelistLink()
time.sleep(3+random.uniform(1, 3)) #备用优化项
print('Phone端新闻类型的参数开始生产...')
productPclistLink()
print('新闻类型的参数完成生产！')
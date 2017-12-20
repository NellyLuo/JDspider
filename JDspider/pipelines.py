# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo import MongoClient
from scrapy.conf import settings
import json
import codecs

c = 0

class JdspiderPipeline(object):
    def __init__(self):
        client = MongoClient()
        MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = client[settings['MONGODB_DB']]
    #待改

    def process_item(self, item, spider):
        # print type(item)
        data = dict(item)
        # print data["pid"]
        collection = self.db[str(data["pid"])]
        collection.insert(json.loads(json.dumps(data)))
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = None

    def process_item(self, item, spider):
        data = dict(item)
        filename = "F:\FakeReview\JDspider\\reviews\\" + data["pid"] + ".txt"
        try:
            self.file = codecs.open(filename, 'a', encoding='utf-8')
        except Exception as e:
            self.file = codecs.open(filename, 'w', encoding='utf-8')
        finally:
            line = json.dumps(dict(item)) + "\n"  # 转为json的
            self.file.write(line.encode("utf-8"))  # 写入文件中
            print "data input ",data["pid"],filename
            pass
        return item

    def spider_closed(self, spider):  # 爬虫结束时关闭文件
        self.file.close()

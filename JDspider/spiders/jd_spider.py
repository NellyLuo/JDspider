# -*- coding: utf-8 -*-
from JDspider.items import JdspiderItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
import scrapy
import random
import json
import time
import os
import re


class JDspider(scrapy.Spider):
    name = "JDspider"
    # allowed_domains = ["JDspider.org"]
    def __init__(self):
        """设置爬取商品代码及获取页数、每个商品评论爬取页数"""
        self.startPage = 1
        self.endPage = 3
        self.cat = '9987,653,655'
        self.setOnly = 1000

    def start_requests(self):
        pages = []

        for i in range(int(self.startPage),int(self.endPage)):
            # url = 'https://list.jd.com/list.html?cat=1315,1343,9719' + '&page=' + str(i) + '&trans=1&JL=6_0_0#J_main'
            url = 'https://list.jd.com/list.html?cat=' + self.cat + '&page=' + str(i) + '&trans=1&JL=6_0_0#J_main'
            page = scrapy.Request(url)
            pages.append(page)
        return pages

    def parse(self, response):
        # print response.body
        xpath_str = "/html/body/div[@id='J_searchWrap']/div[@id='J_container']/div[@id='J_main']/div[@class='m-list']//a[@target='_blank']"
        product_id = response.selector.xpath(xpath_str).re(r'<a target="_blank" href="//item.jd.com/(.*).html">')
        # print product_id
        host = "https://sclub.jd.com/comment/productPageComments.action?productId="
        params_part1 = "&score=0&sortType=3&page="
        params_part2 = "&pageSize=10&callback=fetchJSON_comment98vv"

        for pid in product_id:
            page = 0
            url = host + str(pid) + params_part1 + str(page) + params_part2 + str(random.randint(1, 9999))
            yield Request(url, callback=self.parse_page0)
            # print url

    def parse_page0(self, response):
        json_str = re.findall(r'\((.*?)\);', response.body)[0]
        # print jsonStr.decode('GBK').encode('UTF-8')
        data = json.loads(json_str.decode('GBK').encode('UTF-8'))

        max_page = data["maxPage"]
        pid = data["productCommentSummary"]["productId"]
        host = "https://sclub.jd.com/comment/productPageComments.action?productId="
        params_part1 = "&score=0&sortType=3&page="
        params_part2 = "&pageSize=10&callback=fetchJSON_comment98vv"

        # print pid
        # if str(pid) == '3726830':
            # for page in range(int(max_page)):
        pageCnt =  (self.setOnly if max_page > self.setOnly else max_page)
        for page in range(int(pageCnt)):
            print "Test1: " + "pid\t" + str(pid) + "\tpage\t" + str(page)
            url = host + str(pid) + params_part1 + str(page) + params_part2 + str(random.randint(1, 9999))
            yield Request(url, callback=self.parse_other_page, dont_filter=False, meta= {'testpid':pid,'testpage':pageCnt})

    def parse_other_page(self, response):
        time.sleep(1)
        try:
            json_str = re.findall(r'\((.*?)\);', response.body)[0]
        except Exception as e:
            print e
            os._exit(0)
        data = json.loads(json_str.decode('GBK').encode('UTF-8'))

        """test"""
        # print jsonStr.decode('GBK').encode('UTF-8')
        # print data["productCommentSummary"]["productId"]
        testpid = response.meta['testpid']
        testpage = response.meta['testpage']
        print "Test2: " + "pid\t" + str(testpid) + "\tpage\t" + str(testpage)
        """test"""

        for item in data["comments"]:
            # temp = JdspiderItem({'id': item["id"], 'content': item["content"], 'userLevelName': item["userLevelName"], 'isMobile': item["isMobile"], 'days': item["days"]})
            temp = JdspiderItem({
                "pid": str(data["productCommentSummary"]["productId"]),
                "uid": str(item["id"]),
                "content": item["content"],
                "creationTime" : str(item["creationTime"]),
                "replyCount" : str(item["replyCount"]),
                "score" : str(item["score"]),
                "usefulVoteCount" : str(item["usefulVoteCount"]),
                "uselessVoteCount" : str(item["uselessVoteCount"]),
                "viewCount" : str(item["viewCount"]),
                "imageCount" : str(item["imageCount"]),
                "userLevelName" : item["userLevelName"].encode("UTF-8"),
                "isMobile" : str(item["isMobile"]),
                "days" : str(item["days"]),
                "afterDays" : str(item["afterDays"])
            })
            # print data["productCommentSummary"]["productId"],item["id"],temp["content"]
            yield temp






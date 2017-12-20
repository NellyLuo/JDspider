# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    pid = scrapy.Field()
    uid = scrapy.Field()
    content = scrapy.Field()
    creationTime = scrapy.Field()
    replyCount = scrapy.Field()
    score = scrapy.Field()
    usefulVoteCount = scrapy.Field()
    uselessVoteCount = scrapy.Field()
    viewCount = scrapy.Field()
    imageCount = scrapy.Field()
    userLevelName = scrapy.Field()
    isMobile = scrapy.Field()
    days = scrapy.Field()
    afterDays = scrapy.Field()
    pass

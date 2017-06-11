# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyuanwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 个人头像链接
    header_url=scrapy.Field()
    # 用户名
    username=scrapy.Field()
    # 内心独白
    monologue=scrapy.Field()
    # 相册图片链接
    pic_urls=scrapy.Field()
    #籍贯
    place_from=scrapy.Field()
    #学历
    education=scrapy.Field()
    # 年龄
    age=scrapy.Field()
    #身高
    height=scrapy.Field()
    #工资
    salary=scrapy.Field()
    #兴趣爱好
    hobby=scrapy.Field()
    # 网站来源 youyuan
    source=scrapy.Field()
    # 个人主页源url
    source_url=scrapy.Field()
    # 爬虫名
    spider=scrapy.Field()


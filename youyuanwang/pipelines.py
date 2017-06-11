# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import json
#
# class YouyuanwangPipeline(object):
#     def __init__(self):
#         self.filename=open("youyuanwang.json","wb")
#     def process_item(self, item, spider):
#         jsontext=json.dumps(dict(item),ensure_ascii=False) + ",\n"
#         self.filename.write(jsontext.encode("utf-8"))
#         return item
#     def close_spider(self,spider):
#         self.filename.close()

import pymysql
from .models.es_types import YouyuanType
class XiciPipeline(object):
    def process_item(self, item, spider):
        # DBKWARGS=spider.settings.get('DBKWARGS')
        con=pymysql.connect(host='127.0.0.1',user='root',passwd='229801',db='yunyuan',charset='utf8')
        cur=con.cursor()
        sql=("insert into youyuanwang(header_url,username,monologue,pic_urls,place_from,education,age,height,salary,hobby,source)"
             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        lis=(item['header_url'],item['username'],item['monologue'],item['pic_urls'],item['place_from'],item['education'],item['age'],item['height'],item['salary'],item['hobby'],item['source'])

        cur.execute(sql,lis)
        con.commit()
        cur.close()
        con.close()
        return item



class ElasticsearchPipeline(object):
    def process_item(self,item,spider):
        youyuan = YouyuanType()
        youyuan.header_url=item["header_url"]
        youyuan.username=item["username"]
        youyuan.age=item["age"]
        youyuan.salary=item["salary"]
        youyuan.monologue=item["monologue"]
        youyuan.pic_urls=item["pic_urls"]
        youyuan.place_from=item["place_from"]

        youyuan.save()

        return item




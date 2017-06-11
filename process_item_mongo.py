#coding=utf-8
__auth__ = 'huwei'
__date__ = '2017/6/4 12:03'

import pymongo
import redis
import json

def process_item():
    Redis_conn=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    Mongo_conn=pymongo.MongoClient(host='127.0.0.1',port=27017)
    db=Mongo_conn["youyuan"]
    table=db["beijing_18_25"]
    while True:
        source, data = Redis_conn.blpop(["youyuan:items"])
        data = json.loads(data.decode("utf-8"))
        table.insert(data)
if __name__=="__main__":
    process_item()

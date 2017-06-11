#coding=utf-8
__auth__ = 'huwei'
__date__ = '2017/6/1 22:08'
import pymysql
import redis
import json

def process_item():
    Redis_conn=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    MySql_conn=pymysql.connect(host='127.0.0.1',user='root',passwd='229801',port=3306,db='yunyuan')
    while True:
        source,data=Redis_conn.blpop("youyuan:items")
        data=json.loads(data.decode("utf-8"))
        cur=MySql_conn.cursor()
        sql=("insert into youyuanwang(header_url,username,monologue,pic_urls,place_from,education,age,height,salary,hobby,source)"
             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (data['header_url'], data['username'], data['monologue'], data['pic_urls'], data['place_from'],
               data['education'], data['age'], data['height'], data['salary'], data['hobby'], data['source'])
        cur.execute(sql,lis)
        MySql_conn.commit()
        cur.close()
        MySql_conn.close()
    if __name__=="__main__":
        process_item()
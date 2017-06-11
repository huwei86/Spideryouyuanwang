# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider
#from scrapy_redis.spiders import RedisCrawlSpider
from youyuanwang.items import YouyuanwangItem


class YouyuanSpider(CrawlSpider):
#class YouyuanSpider(RedisCrawlSpider):
    name = 'youyuan'
    allowed_domains = ['www.youyuan.com']
    # 有缘网的列表页
    start_urls = ['http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1/']
    #redis_key = 'YouyuanSpider:start_urls'
    #动态域范围的获取
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(YouyuanSpider, self).__init__(*args, **kwargs)
    #匹配全国
    #list_page = LinkExtractor(allow=(r'http://www.youyuan.com/find/.+'))
    # 只匹配北京、18~25岁、女性 的 搜索页面匹配规则，根据response提取链接
    page_links=LinkExtractor(allow=r"http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p\d+/")
    # 个人主页 匹配规则，根据response提取链接
    profile_page=LinkExtractor(allow=r"http://www.youyuan.com/\d+-profile/")

    rules = (
        # 匹配列表页成功，跟进链接，跳板
        Rule(page_links),
        # 匹配个人主页的链接，形成request保存到redis中等待调度，一旦有响应则调用parse_profile_page()回调函数处理，不做继续跟进
        Rule(profile_page,callback="parse_profile_page",follow=False)
    )

    # 处理个人主页信息，得到我们要的数据
    def parse_profile_page(self, response):
        item=YouyuanwangItem()
        # 个人头像链接
        item['header_url']=self.get_header_url(response)
        # 用户名
        item['username']=self.get_username(response)
        #籍贯
        item['place_from']=self.get_place_from(response)
        #学历
        item['education']=self.get_education(response)

        # 年龄
        item['age']=self.get_age(response)
        # 身高
        item['height']=self.get_height(response)
        # 工资
        item['salary']=self.get_salary(response)
        # 兴趣爱好
        item['hobby']=self.get_hobby(response)
        # 相册图片链接
        item['pic_urls'] = self.get_pic_urls(response)
        # 内心独白
        item['monologue'] = self.get_monologue(response)
        # 个人主页源url
        item['source_url']=response.url
        # 网站来源 youyuan
        item['source']="youyuan"
        # 爬虫名
        item['spider']="youyuan"
        yield item
   #提取头像地址
    def get_header_url(self,response):
        header=response.xpath('//dl[@class="personal_cen"]/dt/img/@src').extract()
        if len(header):
            header_url=header[0]
        else:
            header_url= ""
        return header_url.strip()
    #提取用户名
    def get_username(self,response):
        username=response.xpath('//dl[@class="personal_cen"]/dd//div[@class="main"]/strong/text()').extract()
        if len(username):
            username=username[0]
        else:
            username=""
        return username.strip()
    #提取年龄
    def get_age(self,response):
        age=response.xpath('//dl[@class="personal_cen"]//p[@class="local"]/text()').extract()
        if len(age):
            age=age[0].split()[1]
        else:
            age=""
        return age
    #提取身高
    def get_height(self,response):
        height=response.xpath('//div[@class="pre_data"]/ul/li[2]/div/ol[2]/li[2]/span/text()').extract()
        if len(height):
            height=height[0]
        else:
            height=""

        return height.strip()
    #提取工资
    def get_salary(self,response):
        salary=response.xpath('//div[@class="pre_data"]/ul/li[2]/div/ol[1]/li[4]/span/text()').extract()
        if len(salary):
            salary=salary[0]
        else:
            salary=""
        return salary.strip()
    #提取兴趣爱好
    def get_hobby(self,response):
        hobby=response.xpath('//dl[@class="personal_cen"]//ol[@class="hoby"]//li/text()').extract()
        if len(hobby):
            hobby=",".join(hobby).replace(" ","")
        else:
            hobby=""
        return hobby.strip()
    #提取相册图片
    def get_pic_urls(self,response):
        pic_urls=response.xpath('//div[@class="ph_show"]/ul/li/a/img/@src').extract()
        if len(pic_urls):
            pic_urls=",".join(pic_urls)
            #将相册url列表转换成字符串
        else:
            pic_urls=""
        return pic_urls
    #提取内心独白
    def get_monologue(self,response):
        monologue=response.xpath('//div[@class="pre_data"]/ul/li/p/text()').extract()
        if len(monologue):
            monologue=monologue[0]
        else:
            monologue=""
        return monologue.strip()
    #提取籍贯
    def get_place_from(self,response):
        place_from=response.xpath('//div[@class="pre_data"]/ul/li[2]/div/ol[1]/li[1]/span/text()').extract()
        if len(place_from):
            place_from=place_from[0]
        else:
            place_from=""
        return place_from.strip()
    #提取学历
    def get_education(self,response):
        education=response.xpath('//div[@class="pre_data"]/ul/li[2]/div/ol[1]/li[3]/span/text()').extract()
        if len(education):
            education=education[0]
        else:
            education=""
        return education.strip()





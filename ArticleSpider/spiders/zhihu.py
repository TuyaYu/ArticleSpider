# -*- coding: utf-8 -*-
#工程目录下 scrapy genspider zhihu www.zhihu.com

import json
import re
import time

import requests
import scrapy
from PIL import Image


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': agent
    }

    print("github")



    def parse(self, response):
        pass


    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin',headers=self.headers,callback = self.login)]




    def login(self,response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text,re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf":xsrf,
                "phone_num":"18710131070",
                "password":"whenever2451",
            }

            return [scrapy.FormRequest(
                url = post_url,
                formdata = post_data,
                headers=self.headers,
                callback=self.check_login

            )]


    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

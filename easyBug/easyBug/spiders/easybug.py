# -*- coding: utf-8 -*-
import scrapy


class EasybugSpider(scrapy.Spider):
    name = 'easybug'
    allowed_domains = ['www.easybug.com','http://easybug.org/Member/Login','http://easybug.org/Bug/AllBug/4745']
    start_urls = ['http://www.easybug.org/Member/Login']
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,self.parse,dont_filter=True)

    def parse(self, response):
        #item = EasybugItem()
        login_url = 'http://easybug.org/Member/Login'
        yield scrapy.FormRequest(
            url=login_url,
            formdata = {
            'email':'luotao@mastercom.cn',
            'Password':'luotao@mastercom.cn'
            },
            callback = self.after_login,
            dont_filter=True
            )
    def after_login(self,response):
        yield scrapy.Request(
            url='http://easybug.org/Bug/AllBug/4745',
            callback=self.parse_page,
            dont_filter=True)
    def parse_page(self,response):
        next_page = response.xpath('/div[@class="PageTop"]/div/table/tbody/tr/td[@style="font-weight:bold"]/span/text()').extract();
        with open("next_page.txt","wb") as f:
            f.write(next_page.decode())
        

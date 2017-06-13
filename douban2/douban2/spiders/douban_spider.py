# -*- coding: utf-8 -*-
import scrapy
from douban2.items import Douban2Item

class DoubanSpiderSpider(scrapy.Spider):
    name = "douban_spider"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['http://movie.douban.com/top250']
    url = 'http://movie.douban.com/top250'
    def start_requsets(self):
    	for url in self.start_urls:
    		yield scrapy.Request(url,self.parse)

    def parse(self, response):
    	item = Douban2Item()

    	Movies = response.xpath('//div[@class="info"]')
    	for eachMovie in Movies:
    		title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
    		fullTitle=''
    		#print(title)
    		for each in title:
    			fullTitle+=each

    		movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
    		star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
    		quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

    		if quote:
    			quote = quote[0]
    		else:
    			quote = ''
    		# print(fullTitle.encode('utf8'))
    		# print(movieInfo)
    		# print(star[0])
    		# print(quote)
    		item['title']=fullTitle
    		item['movieInfo']=';'.join(movieInfo)
    		item['star'] = star[0]
    		item['quote'] = quote
    		yield item
    		next_link = response.xpath('//span[@class="next"]/a/@href').extract()
    		if next_link:
    			nextLink=next_link[0]
    			print(nextLink)
    			yield scrapy.Request(self.url+nextLink,self.parse)
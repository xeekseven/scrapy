import scrapy
from douban2.items import ZhihuItem
import time
from io import StringIO

try:
    from PIL import Image
except:
    pass

class  ZhihuSpider(scrapy.Spider):
	"""docstring for  ZhihuSpider"""
	name = "zhihu"
	allowed_domains = ["www.zhihu.com"]
	start_urls = ['https://www.zhihu.com/']

	headers = {
	"Accept": "*/*",
	"Accept-Encoding": "gzip,deflate",
	"Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
	"Connection": "keep-alive",
	"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
	"Referer": "http://www.zhihu.com/"
	}



	def start_requests(self):
		# yield self.get_captcha()
		cookies = {
		"d_c0":"",
		"l_cap_id":"",
		"r_cap_id":"",
		"cap_id":"",
		"_zap":"",
		"__utmc":"",
		"__utmb":"",
		"__utmv":"",
		"__utma":"",
		"__utmz":"",
		"q_c1":"",
		"_ga":"",
		"_xsrf":"",
		"l_n_c":"",
		"n_c":"",
		"unlock_ticket":"",
		"z_c0":"" }
		return [scrapy.Request('https://www.zhihu.com/#signin',meta={'cookiejar':1},callback=self.post_login)]
	
	def post_login(self,response):
		xsrf_array = response.xpath('//input[@name="_xsrf"]/@value').extract()

		xsrf = xsrf_array[0]
		t = str(int(time.time()*1000))
		captcha_url='http://www.zhihu.com/captcha.gif?r='+t+"&type=login"
		yield scrapy.Request(
			url=captcha_url,
			headers=self.headers,
			meta={
				'cookiejar':response.meta['cookiejar'],
				'_xsrf':xsrf
			},
			callback=self.save_captcha)
		# captcha=self.get_captcha()
		# print("captcha:")
		# print(captcha)
		# print(response)
		# return scrapy.FormRequest(
		# 	url='https://www.zhihu.com/login/email',
		# 	method="POST",
		# 	meta = { 
		# 		'cookiejar':response.meta['cookiejar'],
		# 		'_xsrf':xsrf
		# 	 },
		# 	headers = self.headers,
		# 	formdata = {
		# 	'_xsrf':xsrf,
		# 	'email':'898570963@qq.com',
		# 	'password':'19950422lt',
		# 	'captcha_type':'cn',

		# 	},
		# 	callback= self.after_login,
			
		# 	)

	def get_captcha(self):
		t = str(int(time.time()*1000))
		captcha_url='http://www.zhihu.com/captcha.gif?r='+t+"&type=login"
		yield scrapy.Request(captcha_url,callback=self.save_captcha)
	def save_captcha(self,response):
		login_url='https://www.zhihu.com/login/email'
		with open("cap.jpg","wb") as f:
			f.write(response.body)
		Image.open('cap.jpg').show()
		print('u输入验证码')
		captcha = input()
		yield scrapy.FormRequest(
			url=login_url,
			headers=self.headers,
			meta ={
				'cookiejar':response.meta['cookiejar'],
			},
			formdata = {
			'_xsrf':response.meta['_xsrf'],
			'email':'898570963@qq.com',
			'password':'19950422lt',
			#'captcha_type':'cn',
			'captcha':captcha
			},
			callback = self.after_login,
			)
		#return input('输入验证码')

	def after_login(self,response):
		print("after_login")
		#print(str(response.body,encoding="utf-8"))

		with open("zhihu.html","wb") as f:
			f.write(response.body)
		for url in self.start_urls:
			yield scrapy.Request(
				url,
				headers=self.headers,
				meta ={
				'cookiejar':response.meta['cookiejar'],
				'dont_redirect': True
				},
				callback=self.parse,
				dont_filter=True
				)

	def parse(self,response):
		print("parse")
		print(response)
		res = response
		with open("zhihuWeb.html","wb") as f:
			f.write(response.body)
		item = ZhihuItem()
		infos = res.xpath('//div[@class="feed-content"]')
		print(res.xpath('//div[@class="feed-content"]'))
		for info in infos:
			title = info.xpath('h2[@class="feed-title"]/a/text()').extract()
			print(title)
			if title != []:
				item['title'] = title[0]
			content = info.xpath('div[@class="expandable entry-body"]/div[@class="zm-item-rich-text expandable js-collapse-body"]/div[@class="zh-summary summary clearfix"]/text()').extract()
			print(content)
			if content != []:
				item['content'] = content[0]
			author = info.xpath('div[@class="expandable entry-body"]/div[@class="zm-item-answer-author-info"]/span/span/a/text()').extract()
			print(author)
			if author != []:
				item['author'] = author[0]
				
			print("here")
			yield item
		
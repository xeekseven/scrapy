# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class Douban2Pipeline(object):
	def __init__(self):
		self.file = open('item2.json',"wb")
	def process_item(self, item, spider):
		line = json.dumps(dict(item))+"\n"
		self.file.write(line.encode(encoding="utf-8"))
		return item
    	# if item['star']:
    	# 	item['star'] = int(item['star'])*10
     #    return item

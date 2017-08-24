# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class EasybugPipeline(object):
    def process_item(self, item, spider):

        return item
    def save_item(self,item):
    	conn = sqlite3.connect('../db/easybug.db')
    	cursor = conn.cursor()
    	cursor.execute()
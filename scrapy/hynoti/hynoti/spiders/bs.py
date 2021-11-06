import scrapy
from ..items import BsItem
from datetime import datetime


# business school spider
class BsSpider(scrapy.Spider):
    name = 'bs'
    allowed_domains =['bizug.hanyang.ac.kr']
    start_urls = ['http://bizug.hanyang.ac.kr/-3']

    def parse(self, response):
        pass
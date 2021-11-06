import scrapy


# mechanical engineering spider
class MeSpider(scrapy.Spider):
    name = 'me'
    allowed_domains = ['me.hanyang.ac.kr']
    start_urls = ['http://me.hanyang.ac.kr/']

    # TODO
    def parse(self, response):
        pass

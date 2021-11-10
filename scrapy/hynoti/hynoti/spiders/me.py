import scrapy
from ..items import MeItem
from datetime import datetime
from ..error import send_email


# mechanical engineering spider
class MeSpider(scrapy.Spider):
    name = 'me'
    allowed_domains = ['me.hanyang.ac.kr']
    start_urls = ['https://me.hanyang.ac.kr/front/bulletin/bulletinSub1']

    def parse(self, response):
        try:
            for li in response.css('#pjax-container > div.wrap > div.content_body > div.crud.board > ul > li'):
                # category = li.css('a > span.subject > span.label::text').get()
                texts = li.css('a > span.subject::text').getall()
                title = list(filter(lambda text: len(text.strip()) != 0, texts))[0].strip()
                date = li.css('a > span.subject > span.datetime::text').get()
                href = li.css('a').attrib['href']
                noticeLink = response.urljoin(href)

                request = scrapy.Request(noticeLink, self.get_content)
                request.cb_kwargs['title'] = title
                request.cb_kwargs['date'] = date
                request.cb_kwargs['noticeLink'] = noticeLink
                yield request
        except Exception:
            send_email('MeSpider parse')

    def get_content(self, response, title, date, noticeLink):
        try:
            file = str()
            content = response.css('#pjax-container > div.wrap > div.content_body > div.board > div > div.box > div.content').get()
            lis = response.css('#pjax-container > div.wrap > div.content_body > div.board > div > div.box > ul.files > li')

            if lis.get():
                for li in lis:
                    fileLink = li.css('a').attrib['href']
                    file += response.urljoin(fileLink) + '|'
                file = file[:-1]
            else:
                file = None

            yield MeItem(
                category='whole',
                title=title,
                writer=None,
                date=self.get_datetime(date),
                noticeLink=noticeLink,
                content=content,
                file=file
            )
        except Exception:
            send_email('MeSpider get_content')
            
    def get_datetime(self, date):
        a = date.strip().split('.')
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        return datetime(year, month, day)

            
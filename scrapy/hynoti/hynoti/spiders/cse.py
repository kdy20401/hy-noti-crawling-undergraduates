import scrapy
from ..items import CseItem
from datetime import datetime


# computer software engineering spider
class CseSpider(scrapy.Spider):
    name = 'cse'
    allowed_domains = ['cs.hanyang.ac.kr']
    start_urls = [
        'http://cs.hanyang.ac.kr/board/info_board.php',  # haksa normal
        'http://cs.hanyang.ac.kr/board/job_board.php',   # recruitment information
    ]

    def get_datetime(self, date):
        a = date.strip().split('.')
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        return datetime(year, month, day)

    def parse(self, response):
        category = response.css('#contentArea > div.tit_area > h3::text').get().replace(' ', '')[:-3]

        for tr in response.css('#content_box > div > table > tbody > tr'):
            title = tr.css('td.left > a::text').get()
            writer = tr.css('td:nth-child(4)::text').get()
            date = tr.css('td:nth-child(5)::text').get()
            noticeLink = tr.css('td.left > a').attrib['href']

            print(title, date)
            continue
        
            # notice is within the domain
            if noticeLink.startswith('/board'):
                request = scrapy.Request(response.urljoin(noticeLink), self.get_content)
                request.cb_kwargs['category'] = category
                request.cb_kwargs['title'] = title
                request.cb_kwargs['writer'] = writer
                request.cb_kwargs['date'] = date
                request.cb_kwargs['noticeLink'] = noticeLink
                yield request
            # notice is outside of the domain
            else:
                yield CseItem(
                    category=category,
                    title=title,
                    writer=writer,
                    date=self.get_datetime(date),
                    noticeLink=noticeLink,
                    content=None,
                    file=None
                )
            
    def get_content(self, response, category, title, writer, date, noticeLink):
        fileLinks = []
        file = str()

        content = response.css('#content_box > div > table.bbs_view > tbody > tr:nth-child(3)').get()
        
        for a in response.css('#content_box > div > table.bbs_view > tbody > tr:nth-child(3) > td > div > a'):
            if 'href' in a.attrib.keys():
                fileLinks.append(response.urljoin(a.attrib['href']))

        for fileLink in fileLinks:
            file += fileLink + '|'
            
        if file == '':
            file = None
        else:
            file = file[:-1]

        yield CseItem(
            category=category,
            title=title,
            writer=writer,
            date=self.get_datetime(date),
            noticeLink=response.urljoin(noticeLink),
            content=content,
            file=file
        )
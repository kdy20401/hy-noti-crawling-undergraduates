import scrapy
from ..items import CseItem


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['cs.hanyang.ac.kr']
    start_urls = [
        'http://cs.hanyang.ac.kr/board/info_board.php?ptype=list&page=1&code=notice',
        'http://cs.hanyang.ac.kr/board/info_board.php?ptype=list&page=2&code=notice',
        'http://cs.hanyang.ac.kr/board/info_board.php?ptype=list&page=3&code=notice',
        'http://cs.hanyang.ac.kr/board/info_board.php?ptype=list&page=4&code=notice',
        'http://cs.hanyang.ac.kr/board/info_board.php?ptype=list&page=5&code=notice',
    ]
    

    def parse(self, response):
        begin = response.url.rfind('/')
        end = response.url.rfind('_')
        category = response.url[begin + 1:end]

        for tr in response.css('#content_box > div > table > tbody > tr'):
            title = tr.css('td.left > a::text').get()
            writer = tr.css('td:nth-child(4)::text').get()
            date = tr.css('td:nth-child(5)::text').get()
            notieLink = tr.css('td.left > a').attrib['href']

            if not notieLink.startswith('/board'):
                print(title)

            
    def get_content(self, response, category, title, writer, date, notieLink):
        fileLinks = []

        content = response.css('#content_box > div > table.bbs_view > tbody > tr:nth-child(3)').get()

        for a in response.css('#content_box > div > table.bbs_view > tbody > tr:nth-child(3) > td > div > a'):
            fileLinks.append(response.urljoin(a.attrib['href']))

        file = str()
        for fileLink in fileLinks:
            file += fileLink + '|'
        file = file[:-1]

        if file == '':
            file = None

        yield CseItem(
            category=category,
            title=title,
            writer=writer,
            date=date,
            noticeLink=notieLink,
            content=content,
            file=file
        )
        

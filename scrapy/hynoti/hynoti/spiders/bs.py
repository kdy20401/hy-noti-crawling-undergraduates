import scrapy, re
from ..items import BsItem
from datetime import datetime
from ..error import send_email


# business school spider
class BsSpider(scrapy.Spider):
    name = 'bs'
    allowed_domains =['bizug.hanyang.ac.kr']
    start_urls = ['https://bizug.hanyang.ac.kr/-3']

    def parse(self, response):
        try:
            p = re.compile('\d+')
            query_string = '?p_p_id=board_WAR_bbsportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&'\
                'p_p_col_count=1&_board_WAR_bbsportlet_sCategoryId=0&_board_WAR_bbsportlet_sDisplayType=1&_board_WAR_bbsportlet_sCurPage=1'\
                '&_board_WAR_bbsportlet_action=view_message&_board_WAR_bbsportlet_messageId='

            for tr in response.css('#p_p_id_board_WAR_bbsportlet_ > div > div > div > div:nth-child(2) > table > tbody > tr'):
                title = tr.css('p.title > a::text').get()
                writer = tr.css('p.info > span::text').get()
                date = tr.css('span.date::text').get()
                href = tr.css('p.title > a').attrib['href'] 
                message_id = p.search(href).group()
                noticeLink = self.start_urls[0] + query_string + message_id

                request = scrapy.Request(noticeLink, self.get_content)
                request.cb_kwargs['title'] = title
                request.cb_kwargs['writer'] = writer
                request.cb_kwargs['date'] = date
                request.cb_kwargs['noticeLink'] = noticeLink
                yield request
        except Exception:
            send_email('BsSpider parse')

    def get_content(self, response, title, writer, date, noticeLink):
        try:
            file = str()
            content = response.css('#p_p_id_board_WAR_bbsportlet_ > div > div > div.bbs.bbs-portlet > div > table > tbody > tr:nth-child(3)').get()
            tr = response.css('#p_p_id_board_WAR_bbsportlet_ > div > div > div.bbs.bbs-portlet > div > table > tbody > tr:nth-child(4)')

            if tr.get():
                for li in tr.css('td > div > ul > li'):
                    fileLink = li.css('i > a').attrib['href']
                    file += fileLink + '|'
                file = file[:-1]
            else:
                file = None

            yield BsItem(
                category='whole',
                title=title,
                writer=writer,
                date=self.get_datetime(date),
                noticeLink=noticeLink,
                content=content,
                file=file
            )
        except:
            send_email('BsSpider get_content')

    def get_datetime(self, date):
        a = date.strip().split('/')
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        return datetime(year, month, day)
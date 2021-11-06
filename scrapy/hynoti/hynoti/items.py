import scrapy


class NoticeItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    writer = scrapy.Field()
    date = scrapy.Field()
    noticeLink = scrapy.Field()
    content = scrapy.Field()
    file = scrapy.Field()


class CseItem(NoticeItem):
    pass


class BsItem(NoticeItem):
    pass
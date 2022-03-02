# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlDataFacebookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CrawlDataFaceBook(scrapy.Item):
    page = scrapy.Field()


class CrawlData(scrapy.Item):
    post = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JuniorOffersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobOfferItem(scrapy.Item):
    company = scrapy.Field()
    position  = scrapy.Field()
    salary = scrapy.Field()
    locations = scrapy.Field()
    logoUrl = scrapy.Field() 
    offerUrl = scrapy.Field()
    companyUrl = scrapy.Field()
    stack = scrapy.Field()

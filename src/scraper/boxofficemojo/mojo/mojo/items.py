# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MojoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    domestic = scrapy.Field()
    foreign = scrapy.Field()
    budget = scrapy.Field()
    runtime = scrapy.Field()
    rating = scrapy.Field()
    genre = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    title = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=float)
    link = scrapy.Field(serializer=str)
    store = scrapy.Field(serializer=str)
    photos = scrapy.Field(serializer=list)
    exchange = scrapy.Field(serializer=str)

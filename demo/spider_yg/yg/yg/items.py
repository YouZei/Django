# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YgItem(scrapy.Item):
    # define the fields for your item here like:
    # 标签，商品spu，商品图片，商品sku，价格，介绍
    tag = scrapy.Field()
    spu = scrapy.Field()
    image_url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    introduction = scrapy.Field()

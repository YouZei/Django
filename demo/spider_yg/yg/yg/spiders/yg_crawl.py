# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
from yg.items import YgItem

import scrapy

class YgCrawlSpider(scrapy.Spider):
    name = 'yg_crawl'
    allowed_domains = ['yiguo.com']
    start_urls = ['http://www.yiguo.com/']
    def parse(self, response):
        div_list = response.xpath("//div[@class='catalogs-list']/div")[:7]  # 获取前7个 大分类
        for index, div in enumerate(div_list):
            item = YgItem()
            a_list = div.xpath(".//div[@class='sub-list']/a")
            # print("a_list",len(a_list))
            for a in a_list:
                if index < 2:
                    item["tag"] = "新鲜水果"  # 新鲜水果  1
                elif index == 2:
                    item["tag"] = "精选肉类"  # 肉  2
                elif index == 3:
                    item["tag"] = "禽类蛋品"  # 蛋     3
                elif index == 4:
                    item["tag"] = "海鲜水产"  # 海鲜   4
                elif index == 5:
                    item["tag"] = "乳品糕点"  # 乳品糕点   5
                else:
                    item["tag"] = "新鲜蔬菜"  # 蔬菜   5

                item["spu"] = a.xpath("./text()").get()
                detail_url = a.xpath("./@href").get()
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"item": deepcopy(item)},)

    def parse_detail(self, response):
        item = deepcopy(response.meta["item"])
        li_list = response.xpath("//div[@class='goods_list clearfix']//li")
        # print("li_list", len(li_list))
        for li in li_list:
            item["image_url"] =  li.xpath(".//div[@class='p_img clearfix']/a/img/@src").get()
            item["name"] = li.xpath(".//div[@class='p_name']/a/text()").get()
            item["price"] = li.xpath(".//div[@class='p_price']/span/strong/text()").get().split("¥")[1]
            item["introduction"] = li.xpath(".//div[@class='p-buy']/span/text()").get()
            yield item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import csv
import os
from scrapy import Request
import re

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from .items import YgItem
from . import settings


class YgPipeline(object):
    """
    数据存储到csv格式里面
    """

    def __init__(self):
        self.file = codecs.open('yg.csv', 'a', encoding='gbk')
        self.wr = csv.writer(self.file)
        self.wr.writerow(['tag', 'spu', 'name', 'price', 'introduction', 'image_url'])  # 先写标题

    def process_item(self, item, spider):
        """
        当spider模块使用yield提交一个数据的时候会调用这个方法
        :param item:
        :param spider:
        :return:
        """
        self.wr.writerow([item['tag'],
                          item['spu'],
                          item['name'],
                          item['price'],
                          item['introduction'],
                          item['image_url'],
                          ])
        return item

    def close_spider(self, spider):
        """
        爬虫关闭的时候会调用这个方法
        :param spider:
        :return:
        """
        # 关闭打开的文件
        self.file.close()


class YgPipelineImageDown(ImagesPipeline):

    # IMAGES_STORE = get_project_settings().get('IMAGES_STORE')  # 获取下载地址

    def get_media_requests(self, item, info):
        if isinstance(item, YgItem):
            yield Request(item["image_url"])

    # def file_path(self, request, response=None, info=None):
    #     tag = request.item['tag']
    #     images_store = settings.IMAGES_STORE
    #     tag_path = os.path.join(images_store, tag)
    #     if not os.path.exists(tag_path):
    #         os.mkdir(tag_path)
    #     image_name = request.item["name"]
    #     image_name = image_name.replace("/", "-").replace("/n", "").replace("\\", "").replace(":", "").replace("*","").replace("?", "")  # 去除非法字符
    #     image_path = os.path.join(tag_path, image_name)
    #     return image_path

    def item_completed(self, results, item, info):
        """更改文件名称"""
        if results[0][0] == True:
            path = results[0][1]['path']

            image_name = re.sub(r'full/.*\.jpg', item["name"] + ".jpg", path)
            image_name = image_name.replace("/", "-").replace("/n", "").replace("\\", "").replace(":", "").replace("*","").replace("?", "")  # 去除非法字符

            s_name = settings.IMAGES_STORE + '/' + path
            d_name = settings.IMAGES_STORE + '/' + image_name
            os.rename(s_name, d_name)  # 改名
            return item




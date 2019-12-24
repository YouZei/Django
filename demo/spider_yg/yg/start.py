# -*- coding: utf-8 -*-
"""
    @Time : 2019/12/22 0:04
    @Author : Lyx
    @File : start.py
    @Software: PyCharm 
"""

from scrapy import cmdline

cmdline.execute('scrapy crawl yg_crawl'.split())

# -*- coding: utf-8 -*-
"""
    @Time : 2019/12/22 11:19
    @Author : Lyx
    @File : utils.py
    @Software: PyCharm 
"""
import csv
import requests
import os

def data_read(path):
    """读取csv"""
    with open(path, newline='', encoding='GBK') as f:
        rows = csv.reader(f)
        data_list = []
        temp_list = None
        for index, row in enumerate(rows):
            if index == 0:  # 读取第一行
                temp_list = row
            data_list.append(dict(zip(temp_list, row)))
        if data_list[0]["name"] == "name":
            data_list.pop(0)  # 删除头部

        # 数据去重
        data_list = [dict(t) for t in set([tuple(d.items()) for d in data_list])]

        return data_list

def image_path():
    """返回图片路径"""
    data_list = data_read("yg.csv")
    for item in data_list:
        image_name = item["name"]
        image_name = image_name.replace("/", "-").replace("/n", "").replace("\\", "").replace(":", "").replace("*","").replace("?", "")  # 去除非法字符


if __name__ == '__main__':
    # print(data_read("yg.csv"))
    pass



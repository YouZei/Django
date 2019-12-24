# -*- coding: utf-8 -*-
"""
    @Time : 2019/12/22 11:14
    @Author : Lyx
    @File : goods_sku_push.py
    @Software: PyCharm 
"""
from selenium import webdriver
from selenium.webdriver.support.select import Select
from utils import data_read
import time
import os

# 获取图片路径
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'images')


driver = webdriver.Chrome()

driver.get("http://127.0.0.1:8000/admin/goods/goodssku/add/")
driver.maximize_window()
time.sleep(10)  # 设置用户名


# driver.add_cookie({'csrftoken':'3OD4A5Mildu8ZSeOHx1bCgwZl383wfr8','sessionid':'zwu5o53co127g1qfe8wco6sc6z8deuhf'})
def push(project,sku,name,introduction,price,unite):
    """
    添加商品spu
    :return:
    """
    # 填充商品商品种类输入框
    Select(driver.find_element_by_id("id_type")).select_by_visible_text(project)

    # 填充商品SPU输入框
    Select(driver.find_element_by_id("id_goods")).select_by_visible_text(sku)

    # 填充商品名称输入框
    element_name = driver.find_element_by_id("id_name")
    element_name.clear()
    element_name.send_keys(name)

    # 填充商品简介输入框
    element_desc = driver.find_element_by_id("id_desc")
    element_desc.clear()
    element_desc.send_keys(introduction)

    # 填充商品价格输入框
    element_price = driver.find_element_by_id("id_price")
    element_price.clear()
    element_price.send_keys(price)

    # 填充商品单位输入框
    element_unite = driver.find_element_by_id("id_unite")
    element_unite.clear()
    element_unite.send_keys(unite)

    # 填充商品库存输入框
    element_stock = driver.find_element_by_id("id_stock")
    element_stock.clear()
    element_stock.send_keys(1000)


    # 填充图片
    # TODO
    image_name = name.replace("/", "-").replace("/n", "").replace("\\", "").replace(":", "").replace("*","").replace("?", "") + ".jpg"  # 去除非法字符
    image_path = os.path.join(IMAGE_PATH,image_name)

    driver.find_element_by_id('id_image').send_keys(image_path)

    # 获取提交按钮
    click_btn = driver.find_element_by_name("_addanother")
    # 点击提交
    click_btn.click()

def unite_parse(name):
    if "g" in name and "kg" not in name:
        unite = "g"
    elif "个" in name :
        unite = "个"
    elif "盒" in name :
        unite = "盒"
    elif "镑" in name :
        unite = "镑"
    else:
        unite = "kg"
    return unite

if __name__ == '__main__':

    data_list = data_read("yg.csv")
    # 填充商品sku信息
    for item in data_list:
        unite = unite_parse(item["name"])
        push(item["tag"], item["spu"],item["name"],item["introduction"],item["price"],unite)
    driver.close()
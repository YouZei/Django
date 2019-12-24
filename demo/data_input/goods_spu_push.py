# -*- coding: utf-8 -*-
"""
    @Time : 2019/12/22 11:14
    @Author : Lyx
    @File : goods_spu_push.py
    @Software: PyCharm 
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from utils import data_read
import time


driver = webdriver.Chrome()

driver.get("http://127.0.0.1:8000/admin/goods/goods/add/")
driver.maximize_window()
time.sleep(10)  # 设置用户名



# driver.add_cookie({'csrftoken':'3OD4A5Mildu8ZSeOHx1bCgwZl383wfr8','sessionid':'zwu5o53co127g1qfe8wco6sc6z8deuhf'})
def push(spu, introduction):
    """
    添加商品spu
    :return:
    """
    # 获取商品SPU名称输入框
    element = driver.find_element_by_id("id_name")

    # 清空
    element.clear()
    # 填充
    element.send_keys(spu)

    # selenium切换到iframe中
    # driver.switchTo().frame("id_detail_ifr")
    driver.switch_to_frame("id_detail_ifr")

    # 获取商品详情输入框
    element2 = driver.find_element_by_id("tinymce")

    # 清空
    element2.clear()
    # 填充
    element2.send_keys(introduction)

    # 从frame中切回主文档
    driver.switch_to.default_content()
    # 获取提交按钮
    click_btn = driver.find_element_by_name("_addanother")
    # 点击提交
    click_btn.click()


if __name__ == '__main__':

    data_list = data_read("yg.csv")
    # 填充商品spu信息
    temp_list = [] # 过滤
    for item in data_list:
        if item["spu"] not in temp_list:
            push(item["spu"], item["introduction"])
            temp_list.append(item["spu"])
            # time.sleep(3)

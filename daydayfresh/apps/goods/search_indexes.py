# -*- coding: utf-8 -*-
"""
    @Time : 2019/12/2 15:01
    @Author : Lyx
    @File : search_indexes.py
    @Software: PyCharm 
"""

# 指定对于某个类的某些数据建立索引
# 索引类名：模型类名+Index

# 定义索引类
from haystack import indexes
# 导入模型类
from goods.models import GoodsSKU


class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段 use_template= True 指定根据表中哪些字段建立索引文件的说明，放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回模型类
        return GoodsSKU

    # 建立索引数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

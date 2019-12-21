# -*- coding: utf-8 -*-
"""
    @Time : 2019/12/21 15:34
    @Author : Lyx
    @File : views.py
    @Software: PyCharm 
"""
from django.shortcuts import render_to_response

def html404(request,**kwargs):
    return render_to_response('error/404.html')
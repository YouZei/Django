from django.conf.urls import url
from .views import  OrderPlaceView,OrderCommitView,OrderPayView,CheckPayView,CommentView,OrderDeleteView

urlpatterns = [
    url(r'^place$',OrderPlaceView.as_view(),name="place"), # 提交订单页面显示
    url(r'^commit$',OrderCommitView.as_view(),name="commit"),# 订单创建
    url(r'^pay$',OrderPayView.as_view(),name="pay"), # 支付宝支付
    url(r'^delete$',OrderDeleteView.as_view(),name="delete"), # 删除订单
    url(r'^check$',CheckPayView.as_view(),name="check"),# 查询支付结果
    url(r'^comment/(?P<order_id>.+)$',CommentView.as_view(),name="comment") # 评论
]

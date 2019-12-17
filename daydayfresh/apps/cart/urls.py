from django.conf.urls import url
from cart.views import CartAddView, CartDeleteView, CartInfoView, CartUpdateView

urlpatterns = [

    url(r'^$', CartInfoView.as_view(), name='show'),  # 购物车页面显示

    url(r'^update$', CartUpdateView.as_view(), name='update'),  # 购物车记录更新

    url(r'^delete$', CartDeleteView.as_view(), name='delete'),  # 购物车记录删除

]

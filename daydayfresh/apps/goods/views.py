from django.shortcuts import render
from django.views.generic import View
from .models import GoodsType, IndexTypeGoodsBanner, IndexPromotionBanner, IndexGoodsBanner


# Create your views here.

class IndexView(View):
    """首页"""

    def get(self, request):
        """显示首页"""

        # 获取商品种类信息
        types = GoodsType.objects.all()

        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')

        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        # 获取首页商品分类信息
        type_goods_banners = IndexTypeGoodsBanner.objects.all()

        # 获取首页分类商品展示信息
        for type in types:  # GoodType
            # 获取type种类首页分类商品的图片展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
            # 获取type种类首页分类商品的文字展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

            # 动态给type添加属性,分别保存分类商品的图片和文字展示信息
            type.image_banners = image_banners
            type.title_banners = title_banners

        # 获取购物车数目
        cart_count = 0

        # 组织上下文
        context = {
            'types': types,
            'goods_banners': goods_banners,
            'promotion_banners': promotion_banners,
            'cart_count': cart_count,
        }
        return render(request, 'index.html', context)

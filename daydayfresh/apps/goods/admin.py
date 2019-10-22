from django.contrib import admin
from goods.models import GoodsType,IndexGoodsBanner,GoodsSKU,Goods,GoodsImage,IndexPromotionBanner,IndexTypeGoodsBanner

# Register your models here.


admin.site.register(GoodsType)
admin.site.register(IndexGoodsBanner)
admin.site.register(GoodsSKU)
admin.site.register(Goods)
admin.site.register(GoodsImage)
admin.site.register(IndexPromotionBanner)
admin.site.register(IndexTypeGoodsBanner)

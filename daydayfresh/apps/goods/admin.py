from django.contrib import admin
from goods.models import GoodsType, IndexGoodsBanner, GoodsSKU, Goods, GoodsImage, IndexPromotionBanner, \
    IndexTypeGoodsBanner
from django.core.cache import cache


# Register your models here.

class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新表数据时调用"""
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker生成新的静态首页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除缓存
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """当数据库有内容删除时会调用"""
        super().delete_model(request, obj)

        # 发出任务，让celery worker生成新的静态首页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除缓存
        cache.delete('index_page_data')


# 继承基类用于在后台页面修改后重新生成缓存
class GoodsTypeAdmin(BaseModelAdmin):
    pass

class IndexGoodsBannerAdmin(BaseModelAdmin):
    list_display = ("sku", "index")


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    list_display = ("type","sku","display_type","index")


class IndexPromotionBannerAdmin(BaseModelAdmin):
    # 注册列表显示字段
    list_display = ("name","url","index")

class GoodsAdmin(BaseModelAdmin):
    """商品SPU管理类"""
    list_display = ("name",)

class GoodsSKUAdmin(BaseModelAdmin):
    """商品"""
    list_display = ("name","price","unite","stock","sales","status")


# 注册后台
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsImage)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)

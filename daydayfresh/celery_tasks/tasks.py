# coding:utf-8
# 使用celery发送邮件
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
from goods.models import GoodsType, IndexTypeGoodsBanner, IndexPromotionBanner, IndexGoodsBanner
import os
from django_redis import get_redis_connection
from django.template import loader, RequestContext

# 在任务处理者(这里放在数据库所在服务器里面)一端加这几句
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daydayfresh.settings")
# django.setup()

# 创建一个Celery实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.0.131:6380/1')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""

    # 组织邮件信息
    subject = '天天生鲜注册信息'
    massage = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)
    send_mail(subject, massage, sender, receiver, html_message=html_message)


@app.task
def generate_static_index_html():
    """产生静态页面"""
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

    # 组织上下文
    context = {
        'types': types,
        'goods_banners': goods_banners,
        'promotion_banners': promotion_banners,
    }

    # 使用模板
    # 1.加载模板文件，返回模板对象
    temp_html = loader.get_template('static_index.html')
    # 2.渲染模板
    static_index_html = temp_html.render(context)
    # 3.生成对应的首页静态文件，保存在worker执行者上
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)

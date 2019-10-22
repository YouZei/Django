# coding:utf-8
# 使用celery发送邮件
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
# 在任务处理者(这里放在数据库所在服务器里面)一端加这几句
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daydayfresh.settings")
# django.setup()

# 创建一个Celery实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.1.200:6379/0')


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

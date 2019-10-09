from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from .models import User
import re


# Create your views here.

# user/register
class RegisterView(View):
    """注册"""

    def get(self, request):
        """普通请求"""
        return render(request, 'register.html')

    def post(self, request):
        """注册处理"""

        # 1. 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2. 进行数据校验

        # 校验数据完整性：
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱：
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验是否勾选协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请勾选协议'})

        # 校验用户名是否已经存在：
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名字不存在
            user = None

        if user:
            # 用户已经存在
            return render(request, 'register.html', {'errmsg': '该用户已经被注册'})

        # 进行业务处理，用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0  # 刚注册的还没有激活
        user.save()

        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/1
        # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode('utf8')  # 指定编码格式,默认utf8可以省略

        # 发送邮件
        send_register_active_email.delay(email, username, token)

        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """进行用户激活"""
        # 进行解密，获取需要激活的用户id
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录界面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已经失效')


# user/login
class LoginView(View):
    """用户登录"""

    def get(self, request):
        """显示登录页面"""
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """登录校验"""
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态,保存在session中
                login(request, user)
                # 获取登录后所要跳转到的地址

                response =  redirect(reverse('goods:index'))

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

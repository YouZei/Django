from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin
from user.models import User, Address
from goods.models import GoodsSKU
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
                # 获取登录后所要跳转到的地址,默认跳转首页
                next_url = request.GET.get('next', reverse('goods:index'))

                response = redirect(next_url)

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


# user/logout
class LogoutView(View):
    """注销"""

    def get(self, request):
        """注销"""
        # 使用logout退出登录用户，会清掉所有session
        logout(request)
        return redirect(reverse('goods:index'))


# user/
class UserInfoView(LoginRequiredMixin, View):
    """用户中心-信息页"""

    def get(self, request):
        """显示"""

        # 获取用户的个人信息
        user = request.user

        # 根据用户获取address信息

        address = Address.objects.get_default_address(user)

        # 获取用户的历史浏览记录
        # 获取StrictRedis对象
        con = get_redis_connection('default')

        # 组织需要存入的list键值格式
        history_key = 'history_%id' % user.id

        # 存入并返回用户浏览的前5个商品的id
        sku_id = con.lrange(history_key, 0, 4)

        # 从数据库查询出具体sku_id对应的商品信息

        # 遍历数据库拿到浏览的前5个商品对象并放入列表
        goods_li = list()
        for id in sku_id:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 定义上下文
        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li}
        return render(request, 'user_center_info.html', context)  # page=user


# user/order
class UserOrderView(LoginRequiredMixin, View):
    """用户中心-订单页"""

    def get(self, request):
        """显示"""

        # 获取用户的订单信息

        return render(request, 'user_center_order.html', {'page': 'order'})  # page=order


# user/address
class UserAddressView(LoginRequiredMixin, View):
    """用户中心-订单页"""

    def get(self, request):
        """显示"""

        # 获取登录用户的user对象
        user = request.user

        # 获取用户的默认地址
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})  # page=address

    def post(self, request):
        """地址的添加"""
        # 接受数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '填写不完整'})
        # 业务处理：地址添加
        if not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机号码不正确'})

        # 如果有默认的地址，添加的新地址不作为默认地址，否则作为默认地址
        # 获取登录用户的user对象
        user = request.user

        address = Address.objects.get_default_address(user)  # 查不到返回none

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user, receiver=receiver, addr=addr, zip_code=zip_code,
                               phone=phone, is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address'))

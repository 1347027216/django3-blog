import time

from django.shortcuts import render

# emil
from .models import EmailVerificationModel
from apps.user.util.Email_Send import Email_Send_Register
from apps.user.util.Email_Send import Email_Send_Forget

# 加密
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# 查询
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

# 登录
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

# 跳转
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import reverse

# view
from django.views.generic.base import View

# from
from .form import UserRegisterForm
from .form import UserLoginForm
from .form import UserPasswordForgetForm
from .form import UserPasswordResetForm

# model
from .models import UserInformationModel
from .models import UserCollectionMode
from apps.blog.models import BlogModel


# 重写类方法根据邮箱和用户名查找
class UserVerificationView(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user_information = UserInformationModel.objects.get(Q(email=username) | Q(username=username))
            if check_password(password, user_information.password):
                return user_information
        except Exception as err:
            return None


# 登录
class UserLoginView(View):

    def get(self, request):
        user_login_form = UserLoginForm()
        return render(request, "sign-in.html", locals())

    def post(self, request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = request.POST.get("Username", "")

            password = request.POST.get("Password", "")

            try:
                user_information = authenticate(username=username, password=password)
                if user_information is not None:

                    if user_information.is_active:
                        login(request, user_information)
                        # 定向跳转到博客主页
                        return HttpResponseRedirect(reverse("blog-index"))

                    else:
                        return render(request, "sign-in.html", {
                            "message": "该用户尚未激活！",
                        })
                else:
                    return render(request, "sign-in.html", {
                        "message": "用户名或密码错误！",
                    })

            except Exception as error:
                return render(request, "sign-in.html", {
                    "message": "未知错误，请与网站管理员联系！",
                })


# 注册
class UserRegisterView(View):
    def get(self, request):
        UserRegister = UserRegisterForm()
        return render(request, "sign-up.html", locals())

    def post(self, request):
        UserRegister = UserRegisterForm(request.POST)
        if UserRegister.is_valid():
            username = request.POST.get("Username", "")
            password = request.POST.get("Password", "")
            rpassword = request.POST.get("rPassword", "")
            if password != rpassword:
                return render(request, "sign-up.html", {
                    "message": "两次密码输入不一致！",
                    "UserRegister": UserRegister,
                })

            if UserInformationModel.objects.filter(email=username):
                return render(request, "sign-up.html", {
                    "message": "该邮箱已被注册！",
                    "UserRegister": UserRegister,
                })

            UserInformation = UserInformationModel()
            UserInformation.email = username
            UserInformation.username = username
            UserInformation.is_active = False
            UserInformation.password = make_password(password)
            UserInformation.save()

            Email_Send_Register(email=username, sendtype="register")

            return render(request, "user-sign-up-turn.html")

        else:
            UserRegister = UserRegisterForm()
            return render(request, "sign-up.html", locals())


# 用户验证
class UserActivateView(View):
    def get(self, request, activate_code):
        all_records = EmailVerificationModel.objects.filter(code=activate_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserInformationModel.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'user-sign-up-activate-fail.html')
        return render(request, 'user-sign-up-activate-succeed.html')


# ajax方法退出登录
class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponse({
            "退出成功！"
        })


# 密码找回
class UserPasswordForgetView(View):
    def get(self, request):
        user_forget_form = UserPasswordForgetForm()
        return render(request, "user-password-forget.html", locals())

    def post(self, request):
        user_forget_form = UserPasswordForgetForm(request.POST)
        if user_forget_form.is_valid():
            username = request.POST.get("Username", "")
            user_information = UserInformationModel.objects.filter(email=username)
            if user_information:
                # 发送验证短信
                Email_Send_Forget(email=username, sendtype="forget")
                return render(request, "user-password-forget-turn.html", {
                    "username": username,
                })


class UserPasswordVerificationView(View):
    def get(self, request, activate_code):
        user_forget_form = UserPasswordForgetForm()
        all_records = EmailVerificationModel.objects.filter(code=activate_code)
        for record in all_records:
            email = record.email
        if all_records:
            return render(request, "user-password-reset.html", {
                "user_forget_form": user_forget_form,
                "username": email,
            })
        else:
            return render(request, "user-password-forget.html", {
                "message": "您的邮箱不正确！",
                "user_forget_form": user_forget_form,

            })


class UserPasswordRestView(View):
    def post(self, request):
        username = request.POST.get("Username", "")
        password = request.POST.get("Password", "")
        rPassword = request.POST.get("rPassword", "")
        if password != rPassword:
            return HttpResponse("两次密码输入不一致！")

        user_information = UserInformationModel.objects.get(email=username)
        user_information.password = make_password(password)
        user_information.save()

        return render(request, "user-password-reset-succeed.html")


class UserCollectionView(View):
    def post(self, request):
        state = request.POST.get("state", "")
        title_id = request.POST.get("title_id", "")
        author = request.POST.get("author", "")
        username = request.user.username
        try:

            title = BlogModel.objects.get(id=title_id).title

        except Exception as err:
            pass
        all_collection = UserCollectionMode.objects.all()
        if state == "收藏":
            user_collect = UserCollectionMode()
            user_collect.username = request.user.username
            user_collect.author = author
            user_collect.title = title
            user_collect.content_id = title_id
            # user_collect.coll_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            user_collect.save()

            return HttpResponse("已收藏")

        else:
            search_dict = dict()
            search_dict["username"] = username
            search_dict["content_id"] = title_id
            UserCollectionMode.objects.filter(**search_dict).delete()
            # print(c)
            return HttpResponse("收藏")


# 个人中心
class UserPersonCenterView(View):
    def get(self, request):
        return render(request, "user-persion-center.html")

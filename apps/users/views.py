# coding=utf8

import os
import json
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect

from users.forms import RegisterForm,LoginForm,ForgetForm,ModifyPwdForm

from users.models import UserProfile,EmailVerfyRecode
from articles.models import Article
from operation.models import UserMessage,ArticleComments
from utils.email_send import send_register_email
from utils.mixin_util import LoginRequiredMixin
from utils.qiniusdk import qiniu_upload_file

from ChenBlog.settings import MEDIA_ROOT
from config import DOMAIN_PREFIX


class IndexView(View):
    def get(self,request):
        article_list = Article.objects.all().order_by('-add_time')
        hot=Article.objects.all().order_by("-comments_nums")[:6]
        click_list = Article.objects.all().order_by('-click_nums')[:6]
        commenter = ArticleComments.objects.all().order_by('-add_time')[:10]
        return render(request,'index.html',{
            'article_list':article_list,
             "click_list":click_list,
            "hot_list":hot,
            'commenter':commenter,
        })


class RegisterView(View):
    # 用户注册处理
    def get(self,request):
        register_form=RegisterForm()
        return render(request,"register.html",{'register_form':register_form})

    def post(self,request):
        register_form=RegisterForm(request.POST)
        pre_check=register_form.is_valid()
        if pre_check:
            user_name=request.POST.get('username','')
            if UserProfile.objects.filter(username=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':u'改名字已被使用'})
            email = request.POST.get('email','')
            if UserProfile.objects.filter(email=email):
                return render(request,'register.html',{"register_form":register_form,'msg':u'该邮箱已被注册'})
            pass_word=request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.username=user_name
            user_profile.email=email
            user_profile.is_active=False
            user_profile.password=make_password(pass_word)
            user_profile.save()

            user_message = UserMessage()
            user_message.user=user_profile.id
            user_message.message = u'欢迎注册陈政伟博客'
            user_message.save()

            send_register_email(email, 'register')
            return render(request, 'send_success.html')

        else:
            return render(request,'register.html',{'register_form':register_form})


class LoginView(View):
    # 处理登录
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request,'login.html',{'msg':u'用户尚未激活,去邮箱激活'})
            else:
                return render(request,'login.html',{'msg':u'用户名或密码错误',})
        else:
            return render(request,'login.html',{'login_form':login_form,})


class LogoutView(View):
    # 退出登陆
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgetView(View):
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'password-forget.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forgetpwd')
            return render(request, 'send_success.html')
        else:
            return render(request,'password-forget.html',{'forget_form':forget_form})


class ResetView(View):
    """
    重置密码页面
    """
    def get(self,request,active_code):
        all_records=EmailVerfyRecode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class ModifyView(View):
    # 用户未登录修改密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('Password1','')
            pwd2=request.POST.get('Password2','')
            email=request.POST.get('email','')
            if pwd1!=pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':u'密码不一致'})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()
            return render(request,'login.html')
        else:
            email=request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'msg':u'密码不一致'})


class ActiveUserView(View):
    def get(self, request, active_code):
        # 用code在数据库中过滤处信息
        all_records = EmailVerfyRecode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # 通过邮箱查找到对应的用户
                user = UserProfile.objects.get(email=email)
                # 激活用户
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class InfoView(LoginRequiredMixin,View):
    # 用户信息
    def get(self,request):
        return render(request,'info.html',)


class UploadImage(LoginRequiredMixin, View):
    def post(self, request):
        # 获取文件后先存在本地，再转存至七牛云
        file_obj = request.FILES.get('file', None)
        file_ext = ""
        if file_obj.name.rfind('.') > 0:
            file_ext = file_obj.name.rsplit('.', 1)[1].strip().lower()
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        path = default_storage.save('' + file_name, ContentFile(file_obj.read()))
        # 保存在本地的临时路径
        temp_file = os.path.join(MEDIA_ROOT, path)

        # 上传到七牛云 返回的是 七牛云上存储的地址
        image_url = qiniu_upload_file(file_name, temp_file)

        # 删除保存在本地的临时文件
        os.remove(temp_file)
        request.user.image = image_url
        request.user.save()
        user=UserProfile.objects.get(username=request.user)

        user.img=image_url

        user.save()
        return HttpResponseRedirect('/userinfo/')


class AboutView(View):
    # 关于作者信息
    def get(self,request):
        return render(request,'about.html')


class SanYanView(View):
    def get(self,request):
        return render(request,'ZaTan.html')
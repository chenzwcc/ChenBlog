# coding=utf8
"""ChenBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
#from django.contrib import admin
import xadmin
from django.views.static import serve
from ChenBlog.settings import MEDIA_ROOT

from users.views import IndexView,LoginView,RegisterView,LogoutView,ResetView,ModifyView,ForgetView,ActiveUserView
from users.views import AboutView,SanYanView


urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    # 后台管理页面
    url(r'^xadmin',include(xadmin.site.urls)),
    # 首页
    url(r'^$',IndexView.as_view(),name='index'),
    # 登录页
    url(r'^login/$',LoginView.as_view(),name='login'),
    # 退出页
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    # 注册页
    url(r'^register/$',RegisterView.as_view(),name='register'),
    # 验证码
    url('^captcha/',include('captcha.urls')),
    # 邮箱激活
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 找回密码
    url(r'^forget/$', ForgetView.as_view(), name="forget_pwd"),
    # 密码重置
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyView.as_view(), name="modify_pwd"),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
    # 用户
    url(r"^userinfo/",include('users.urls',namespace='userinfo')),
    # 关于作者
    url(r"^about/$",AboutView.as_view(),name='about'),
    # 三言两语
    url(r"^sanyan/$", SanYanView.as_view(), name='sanyan'),
    # 文章
    url(r"^article/",include('articles.urls',namespace='article')),



]

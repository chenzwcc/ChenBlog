#coding=utf8
from django.conf.urls import url
from .views import UploadImage,InfoView

urlpatterns = [
    #用户页
    url(r"^$",InfoView.as_view(),name='userinfo'),
    # 用户上传头像
    url(r"^upload/$", UploadImage.as_view(), name='upload'),

]
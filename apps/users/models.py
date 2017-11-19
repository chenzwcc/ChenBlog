# coding=utf8
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):

    #img = models.ImageField(max_length=200,verbose_name=u'头像地址',upload_to='user_img/',default='/people.jpg')
    img = models.CharField(max_length=200, verbose_name='用户头像的七牛云地址',
                             default='http://ozn6w9pxx.bkt.clouddn.com/QQ.jpg')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.username


class EmailVerfyRecode(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email =models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(choices=(("register",u'注册'),('forgetpwd',u'找回密码')),max_length=10,verbose_name=u'发送类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name=u'邮箱验证码'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return "{0}({1})",format(self.code,self.email)


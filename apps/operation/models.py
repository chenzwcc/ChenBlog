#coding=utf8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from articles.models import Article
# Create your models here.


class ArticleComments(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    article = models.ForeignKey(Article,verbose_name=u'文章')
    comments = models.CharField(max_length=300,verbose_name=u'评论内容')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name='文章评论'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.comments


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户')
    message = models.CharField(max_length=500, verbose_name=u'用户消息')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(self.user)
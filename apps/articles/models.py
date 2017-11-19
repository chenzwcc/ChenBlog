#coding=utf-8
from datetime import datetime
from django.db import models

# Create your models here.

class Article(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=100,verbose_name=u'标题名')
    name = models.CharField(max_length=100,verbose_name=u'作者')
    content = models.TextField(verbose_name=u'内容')
    type_id = models.IntegerField(default=1,verbose_name=u'文章类别ID')
    type = models.IntegerField(choices=((1,u'Python'),(2,u'Django'),(3,u'爬虫'),(4,u'Tornado'),(5,u'Flask'),(6,u'AI'),(7,u'数据库'),(8,u'其他')),verbose_name=u'文章类型')
    click_nums = models.IntegerField(default=0,verbose_name=u'浏览量')
    comments_nums = models.IntegerField(default=0,verbose_name=u'评论量')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name=u'文章'
        verbose_name_plural=verbose_name

    # 获取文章的评论量
    def get_comments_nums(self):
        return self.articlecomments_set.all().count()
    # 得到文章的全部评论
    def get_comments(self):
        return self.articlecomments_set.all()


    def __unicode__(self):
        return self.title

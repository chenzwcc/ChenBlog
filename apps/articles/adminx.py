# coding=utf-8

import xadmin

from .models import Article


class ArticleAdmin(object):
    # 添加字段显示
    list_display = ['title', 'name', 'type', 'click_nums','comments_nums','add_time']
    # 添加搜索字段
    search_fields = ['title', 'name', 'type', 'add_time', 'click_nums']
    # 添加过滤字段
    list_filter = ['title', 'name', 'type', 'click_nums', 'add_time']

xadmin.site.register(Article, ArticleAdmin)
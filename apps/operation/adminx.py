# coding=utf8

import xadmin

from .models import ArticleComments, UserMessage


class ArticleCommentsAdmin(object):
    list_display = ['user', 'article', 'comments', 'add_time']
    search_fields = ['user', 'article', 'comments']
    list_filter = ['user', 'article', 'comments', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']



xadmin.site.register(ArticleComments, ArticleCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
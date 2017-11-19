# coding=utf8
from django.conf.urls import url
from articles.views import ArticleView,ArticleDetailView,WriteView,AddCommentsView
urlpatterns= [

    #url(r'^$',ArticleView.as_view(),name='article'),
    # 对应科页面
    url(r'^(?P<type_id>\d+)/$', ArticleView.as_view(), name='article_type'),
    # 对应科页面详情页
    url(r'^(?P<type_id>\d+)/(?P<num_id>\d+)',ArticleDetailView.as_view(),name='article_detail'),
    # 留言也
    url(r'^write/$',WriteView.as_view(),name='write'),
    # 评论
    url(r"^addcomment/$",AddCommentsView.as_view(),name='add_comment'),
]
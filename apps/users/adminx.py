# coding=utf8
import xadmin
from xadmin import views

from .models import EmailVerfyRecode


class BaseSetting(object):
    # 增加主题样式
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = 'ChenBlog后台管理系统'
    siter_footer = '版权所有:陈政伟'
    # 菜单收缩
    menu_style = 'accordion'


class EmailVerfyRecodeAdmin(object):
    # 添加字段显示
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 添加搜索字段
    search_fields = ['code', 'email', 'send_type']
    # 添加过滤字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)
xadmin.site.register(EmailVerfyRecode, EmailVerfyRecodeAdmin)
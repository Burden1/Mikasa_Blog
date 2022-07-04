"""
    xadmin后台注册
"""
# Register your models here.
import xadmin
from article.models import Tag, Article
from user.models import UserProfile


class ArticleAdmin(object):
    list_display = ['title', 'click_num', 'love_num', 'user']
    search_fields = ['title', 'id']
    list_editable = ['click_num', 'love_num']
    list_filter = ['data', 'user']


# xadmin.site.register(UserProfile)
xadmin.site.register(Tag)
xadmin.site.register(Article)

"""
    与文章相关的路由配置在这儿
"""
from django.urls import path

from article.views import article_detail, article_show, write_article, article_comment, slow_life

app_name = 'article'

urlpatterns = [
    # 文章详情
    path('detail', article_detail, name='detail'),
    # 学无止境列表
    path('show', article_show, name='show'),
    # 评论
    path('comment', article_comment, name='comment'),
    # 慢生活
    path('slow_life', slow_life, name='slow_life'),

    # 写博客
    path('write_article', write_article, name='write_article'),

]

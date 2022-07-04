import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from article.forms import ArticleForm
from article.models import Article, Tag, Comment

"""
    文章相关视图函数
"""


def article_detail(request):
    """
    通过id查看文章详情
    :param request:
    :return:
    """
    # 拿到当前文章id
    article_id = request.GET.get('id')
    # print("当前文章id类型：", type(article_id))
    # 根据id拿到当前文章
    current_article = Article.objects.get(pk=article_id)

    # 1、浏览量同步新增：点击一次，浏览量同步加1
    current_article.click_num += 1
    current_article.save()

    # 2、查询相关文章：即对应标签里的前6条数据
    tags_list = current_article.tags.all()  # 首先拿到标签列表
    # 定义【相关文章】list
    about_article_list = []
    for tag in tags_list:
        # 遍历拿到该文章对应标签里的文章列表
        for about_article in tag.article_set.all():
            # 文章不存在list里且少于6篇，则放到list中
            if about_article not in about_article_list and len(about_article_list) < 6:
                about_article_list.append(about_article)
    # print("about_article_list:", about_article_list)

    # 3、拿到上一篇/下一篇文章对象
    all_article = Article.objects.all()  # 拿到所有文章
    # print("all_article:", all_article)
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    # enumerate将其组成一个索引序列，利用它可以同时获得索引和值
    for index, article in enumerate(all_article):
        # 当index为0，即当前文章为第一篇，第一篇文章没有上一篇，默认索引为0，下一篇则为index+1
        if index == 0:
            previous_index = 0
            next_index = index + 1
        # 当index为总长度-1时，即当前文章为最后一篇，上一篇为index-1，下一篇为当前文章
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        # 否则，当index有上一篇/下一篇时，上一篇为index-1，下一篇为index+1
        else:
            previous_index = index - 1
            next_index = index + 1

        # 如果遍历的id等于当前文章详情的id,这里踩了个坑
        if int(article_id) == article.id:
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]

    # 4、根据文章id查询文章评论数
    comments = Comment.objects.filter(article_id=article_id)

    return render(request, 'article/info.html',
                  context={'current_article': current_article, 'about_article_list': about_article_list,
                           'previous_article': previous_article, 'next_article': next_article,
                           'comments': comments})


def article_show(request):
    """
    学无止境列表：进行分页查询
    :param request:
    :return:
    """
    tags = Tag.objects.all()[:6]  # 拿到前6个标签
    tid = request.GET.get('tid')  # 拿到请求的标签id
    if tid:
        # 如果参数传了标签id，拿到当前标签，然后通过当前标签拿到对应标签的所有的文章
        tag = Tag.objects.get(pk=tid)
        print("tag：", tag)
        articles = tag.article_set.all()
        print("通过标签查询到的所有文章：", articles)
    else:
        # 如果参数没传标签id，则查询所有文章
        articles = Article.objects.all()  # 拿到所有的文章

    # 进行分页
    paginator = Paginator(articles, 3)  # Paginator(对象列表，每页几条记录)
    print("文章总数：", paginator.count)  # 文章总数
    print("总页数：", paginator.num_pages)  # 页码
    print("每页篇数：", paginator.page_range)  # 每页多少篇

    # 方法：get_page()
    page = request.GET.get('page', 1)
    page = paginator.get_page(page)  # 这里返回的是page对象
    # page.has_next()  # 有没有下一页
    # page.has_previous()  # 判断是否存在前一页
    # page.next_page_number()  # 获取下一页的页码数
    # page.previous_page_number()  # 获取前一页的页码数

    # 属性：
    # object_list ：当前页的所有对象
    # number ： 当前的页码数
    # paginator: 分页器对象
    return render(request, 'article/learn.html', context={'page': page, 'tags': tags, 'tid': tid})


# 写博客需要用户登录后才可以进行操作，所以需要拦截
@login_required
def write_article(request):
    """
    写博客
    :param request:
    :return:
    """
    if request.method == 'GET':
        aform = ArticleForm()
        return render(request, 'article/write_article.html', context={'form': aform})
    else:
        aform = ArticleForm(request.POST)
        print(aform)
        # 表单校验成功
        if aform.is_valid():
            print("--------->校验成功")
            # 将值保存数据库
            data = aform.cleaned_data
            article = Article()
            article.title = data.get('title')
            article.description = data.get('description')
            article.content = data.get('content')
            # 因为正常情况下，写博客不需要可以设置初始点击量和点赞数，所以我们这里就不需要保存
            # article.click_num = data.get('click_num')
            # article.love_num = data.get('love_num')
            article.image = data.get('image')
            article.user = data.get('user')
            article.save()

            # 标签和文章是多对多关系，必须在文章保存的后面进行添加，否则会报错
            article.tags.set(data.get('tags'))
            print("tags:", data.get('tags'))

            return redirect(reversed('index'))
        else:
            print("--------->校验失败")
        return HttpResponse('test')


def article_comment(request):
    """
    文章评论
    :param request:
    :return:
    """
    # 拿到前端传的值
    nickname = request.GET.get('nickname')
    content = request.GET.get('saytext')
    aid = request.GET.get('aid')
    # 保存数据库
    comment = Comment.objects.create(nickname=nickname, content=content, article_id=aid)
    if comment:
        data = {'status': 1}
    else:
        data = {'status': 0}
    return JsonResponse(data)


def slow_life(request):
    """
    返回【慢生活】页面
    :param request:
    :return:
    """
    # 拿到：慢生活标签的前4篇文章
    tag = Tag.objects.get(name="慢生活")
    slow_articles = tag.article_set.all()[:4]
    print("slow_articles", slow_articles)
    return render(request, 'article/slow_life.html', context={'slow_articles': slow_articles})

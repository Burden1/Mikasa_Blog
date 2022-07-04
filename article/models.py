from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.

# 思考好一篇文章详情内的元素，然后建表
# 例如：标题、描述、内容、标签、发表日期、图片、作者、点赞数、点击量
from user.models import UserProfile


class Tag(models.Model):
    """
        标签表
    """
    name = models.CharField(max_length=50, verbose_name='标签名称')

    def __str__(self):
        return self.name

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准.
    class Meta:
        db_table = 'tag'  # 数据库表名
        verbose_name = '标签'  # 单复数名称
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
        文章表
    """
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.CharField(max_length=300, verbose_name="简介")

    # 原来这里我们是使用TextField属性，现在我们改为使用富文本编辑器：RichTextUploadingField
    content = models.TextField(verbose_name="内容")
    # content = RichTextUploadingField(verbose_name="内容")

    date = models.DateField(auto_now=True, verbose_name="发表日期")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    love_num = models.IntegerField(default=0, verbose_name="点赞量")
    #  todo 这里为什么要加？
    # image = models.ImageField(upload_to='uploads/article/%Y/%m/%d', verbose_name="文章图片",
    #                           default='uploads/article/2022/06/30/photos2.jpg')
    image = models.ImageField(upload_to='uploads/article/%Y/%m/%d', verbose_name="文章图片")

    tags = models.ManyToManyField(to=Tag, verbose_name="标签")  # 标签和文章是多对多关系
    # on_delete=models.CASCADE ：级联删除：当删除主表的数据的时候从表中的数据也随着一起删除。
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, verbose_name="用户")  # 用户和文章是一对多关系

    def __str__(self):
        return self.title

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准.
    class Meta:
        db_table = 'article'  # 数据库表名
        verbose_name = '文章'  # 单复数名称
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
        文章评论表
    """
    # 要添加null=True，不添加的话进行迁移数据库的时候会报错
    nickname = models.CharField(verbose_name='昵称', max_length=16, null=True)
    content = models.CharField(verbose_name='内容', max_length=240)
    create_time = models.DateTimeField(verbose_name='评论时间', auto_now=True)
    # 文章和评论为一对多
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'article_comment'
        verbose_name = "评论"
        verbose_name_plural = verbose_name

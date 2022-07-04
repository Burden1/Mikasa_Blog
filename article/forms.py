from django import forms
from article.models import Article

"""
    文章表单
"""


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        # 将点击量/点赞数给排除掉,不显示
        exclude = ['click_num', 'love_num']

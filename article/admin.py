from django.contrib import admin

# Register your models here.
from article.models import Tag, Article
from user.models import UserProfile

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Article)

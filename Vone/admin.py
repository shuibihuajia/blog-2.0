from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Article)
admin.site.register(Article2Tag)
admin.site.register(ArticleDetail)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ArticleUpDown)
admin.site.register(Tag)
admin.site.register(Blog)
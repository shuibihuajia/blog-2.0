from django import template
register = template.Library()
from ..models import *
from django.db.models import Count


@register.inclusion_tag("menu.html")
def get_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    # 对博客进行分组
    category = Category.objects.filter(blog=blog)
    category_list = category.annotate(c=Count("article")).values_list("title", "c")
    # 数出个人博客下面所有的标签
    tag = Tag.objects.filter(blog=blog)
    tag_list = tag.annotate(c=Count("article")).values_list("title", "c")
    #使用regroup
    # date_list = Article.objects.values("title", "create_time")
    date_list = Article.objects.filter(user=user) \
        .extra(select={"create_month": "DATE_FORMAT(create_time,'%%Y-%%m')"}) \
        .values("create_month").annotate(c=Count("nid")).values_list("create_month", "c")
    return { "user":user, "username": username, "category_list": category_list, "tag_list": tag_list, "date_list": date_list}
from django.conf.urls import url
from Vone import views

urlpatterns = [
    url("poll/$", views.poll),
    # 分类模块，传递参数url
    url("comment/$", views.comment),
    url("backend/$", views.backend),
    url("backend/add_article/$", views.add_article),
    url("get_comment_tree/(\d+)$", views.get_comment_tree),
    url("(?P<username>\w+)/(?P<condition>tag|cate|date)/(?P<param>.*)/", views.homesite, ),
    # 文章详情页
    url("(?P<username>\w+)/articles/(?P<article_id>\d+)/$", views.article_detail),
    # 个人主页
    url("(?P<username>\w+)/$", views.homesite),

]

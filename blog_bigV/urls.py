from django.conf.urls import url,include
from django.contrib import admin
from Vone import views
from django.views.static import serve
from blog_bigV import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^get_valid_img/', views.get_valid_img),
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r"reg/", views.reg),
    url(r"blog/",include("Vone.urls")),
    #url(r"date/", views.month_year),


# media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^upload_img/', views.upload_img),
]


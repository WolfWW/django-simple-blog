#-*- coding:utf-8 -*-

from django.conf.urls import url
from blog import views

app_name = 'blog'
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^article/(?P<article_id>\d+)$',views.ArticleView.as_view(),name='detail'),
    url(r'^category/(?P<category_id>\d+)$',views.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<tag_id>\d+)$',views.TagView.as_view(),name='tag'),
    url(r'^article/(?P<article_id>\d+)/comment/$',views.CommentView.as_view(),name='comment'),
    url(r'^search/$',views.search,name='search'),
    url(r'^all/$',views.AllView.as_view(),name='all'),
]
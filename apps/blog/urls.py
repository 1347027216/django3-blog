

from django.urls import path

from .views import *

# 缓存服务
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(BlogView.as_view()), name="blog-index"),

    path('about/', BlogAboutView.as_view(), name="blog-about"),

    path('author/', BlogAuthorView.as_view(), name="blog-author"),

    path('markdown/', MarkdownBlogView.as_view(), name="blog-write"),

]
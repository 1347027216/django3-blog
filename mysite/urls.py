"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from apps.index.views import IndexView
from django.urls import include

from mysite.settings import MEDIA_ROOT
from mysite.settings import MEDIA_URL
from django.views.static import serve

# 缓存服务
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  cache_page(1)(IndexView.as_view()), name="index"),
    path('user/', include("apps.user.urls")),

    path('search/', include("apps.search.urls")),

    # capthca
    path('captcha/', include('captcha.urls')),

    # blog
    path('blog/', include('apps.blog.urls')),

    # MEDIA_URL配置
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('mdeditor/', include('mdeditor.urls')),
]

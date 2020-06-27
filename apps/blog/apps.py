from django.apps import AppConfig


class BlogConfig(AppConfig):
    #  不能为名称，应该是app的路径
    name = 'apps.blog'
    verbose_name = "博客"
    verbose_name_plural = verbose_name
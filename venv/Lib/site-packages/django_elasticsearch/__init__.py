from django.utils.module_loading import autodiscover_modules

from .documents import Document
from .fields import *
from .indices import Index


def autodiscover():
    autodiscover_modules("documents")


default_app_config = "django_elasticsearch.apps.DEDConfig"

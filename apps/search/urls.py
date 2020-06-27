

from django.urls import path

from .views import *


urlpatterns = [
    path('', BlogSearchView.as_view(), name="blog-search"),

    path('suggest/', SearchSuggestView.as_view(), name="search-suggest"),

]
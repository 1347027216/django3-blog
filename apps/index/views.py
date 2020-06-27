from django.shortcuts import render
from django.views.generic import View
# Create your views here.

from apps.blog.models import BlogModel
from apps.blog.models import CategoryModel


class IndexView(View):
    def get(self, request):
        blog = BlogModel.objects.all().order_by("favorite")[:6]
        return render(request, "index.html", {
            "blog": blog,
        })

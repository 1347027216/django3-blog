import time

from django.shortcuts import render
from django.views.generic import View

from django.core import serializers  # query对象转换

from django.db.models import Q

from django.http import HttpResponse

from apps.blog.models import BlogModel

from django.shortcuts import render
from django.views.generic import View

from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.user.models import UserInformationModel

import markdown

from .form import MDEditorForm

from .models import BlogModel
from .models import CategoryModel
from apps.user.models import UserCollectionMode


class BlogView(View):

    def get(self, request):
        # 获取所有文章
        all_content = BlogModel.objects.all().order_by("-create_time")
        # 获取前端的文章id
        title_id = request.GET.get("title", "")

        # 获取分类信息
        blog_category = request.GET.get("category", "")
        if blog_category:
            blog_category_id = CategoryModel.objects.get(category=blog_category).id
            all_content = BlogModel.objects.filter(category_id=blog_category_id)

        # 获取文章分类
        category = CategoryModel.objects.all()

        # 获取热门文章
        hot_content = BlogModel.objects.all().order_by("favorite")[:5]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_content, 15, request=request)
        # 分页
        page = p.page(page)
        # 分页结束

        if title_id:
            blog = BlogModel.objects.get(id=int(title_id))
            body = markdown.markdown(blog.content.replace("\r\n", '\n\n'), extensions=[
                # 包含 缩写、表格等常用扩展
                'markdown.extensions.extra',
                # 语法高亮扩展
                'markdown.extensions.codehilite',
                # 自动生成目录
                'markdown.extensions.toc',
            ], safe_mode=True, enable_attributes=False)

            user_information = UserInformationModel.objects.get(username=blog.username)
            # 获取用户其他的文章，根据用户名查找用户的其他文章
            more = BlogModel.objects.filter(username=blog.username)[:5]
            # 文章总数
            contents = BlogModel.objects.filter(username=blog.username).count()

            # 根据用户名和title_id查询收藏表

            search_dict = dict()
            search_dict["username"] = request.user.username
            search_dict["content_id"] = blog.id
            # 用户收藏状态查询
            user_coll = UserCollectionMode.objects.filter(**search_dict).count()
            if user_coll:
                return render(request, "blog-content.html", {
                    "blog_information": blog,
                    "title": blog.title,
                    # 转码后的文章内容
                    "content": body,
                    "user_information": user_information,
                    "more": more,
                    # 作品数
                    "contents": contents,
                    # 用户收藏状态
                    "user_collect": 1,
                })
            else:
                return render(request, "blog-content.html", {
                    "blog_information": blog,
                    "title": blog.title,
                    # 转码后的文章内容
                    "content": body,
                    "user_information": user_information,
                    "more": more,
                    # 作品数
                    "contents": contents,
                    # 用户收藏状态
                    "user_collect": 0,
                })
        return render(request, "blog-index.html", {
            "all_content": page,
            "category": category,
            "hot": hot_content,
            "blog_category": blog_category,
        })


class MarkdownBlogView(View):
    def get(self, request):
        template = MDEditorForm()
        all_category = CategoryModel.objects.all()
        return render(request, "blog-upload.html", locals())

    def post(self, request):
        content_form = MDEditorForm(request.POST)
        if content_form.is_valid():
            title = request.POST.get("title", "")

            content = request.POST.get("content", "")

            username = request.user.username

            category = request.POST.get("category", "")

            describle = content[:50] + "..."

            # category_id = self.CategoryFitter(category)
            #
            all_category = CategoryModel.objects.filter(category=category)
            if not all_category:
                new_category = CategoryModel()
                new_category.category = category
                new_category.save()

                new_all_category = CategoryModel.objects.filter(category=category)
                for i in new_all_category:
                    category_id = i.id

                    blog_file = BlogModel()
                    blog_file.title = title
                    blog_file.content = content
                    blog_file.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    blog_file.username = username
                    blog_file.describe = describle
                    blog_file.category_id = category_id
                    blog_file.save()
                    return HttpResponseRedirect(reverse('blog-index'))

            else:
                for category in all_category:
                    category_id = category.id
                    blog_file = BlogModel()
                    blog_file.title = title
                    blog_file.content = content
                    blog_file.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    blog_file.username = username
                    blog_file.describe = describle
                    blog_file.category_id = category_id
                    blog_file.save()
                    return HttpResponseRedirect(reverse('blog-index'))

        return HttpResponseRedirect(reverse('blog-write'))


class BlogAboutView(View):
    def get(self, request):
        return render(request, "blog-about.html")





class BlogAuthorView(View):
    def get(self,request):
        username = request.GET.get("author","")
        blog = BlogModel.objects.filter(username=username)
        hot_content = BlogModel.objects.filter(username=username).order_by("favorite")

        return render(request,"blog-author.html",
        {
            "author":username,
            "all_content":blog,
            "hot":hot_content
        })
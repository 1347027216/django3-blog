from django.contrib import admin

from .models import BlogModel

from .models import CategoryModel

# from .models import BlogModel


class BlogModelAdmin(admin.ModelAdmin):

    list_display = ("id",'title', 'username', 'content', 'create_time', 'favorite', "category")

    search_fields = ['title', 'username', 'category', ]

    list_filter = ('title', 'username', 'content', 'create_time', 'favorite', "category")


admin.site.register(BlogModel, BlogModelAdmin)
admin.site.register(CategoryModel)


class GlobaSettings(object):
    site_title = '彩虹海'
    site_footer = "彩虹海"


admin.site.site_title = "彩虹海"
admin.site.site_header = "彩虹海"
admin.site.index_title = "彩虹海"


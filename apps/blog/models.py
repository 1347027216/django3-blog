from django.db import models

from datetime import datetime

from mdeditor.fields import MDTextField


class CategoryModel(models.Model):
    category = models.CharField(max_length=20, verbose_name=u"文章分类")

    class Meta:
        verbose_name = u'文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class BlogModel(models.Model):
    title = models.CharField(max_length=200,verbose_name=u"标题",null=True)
    create_time = models.DateTimeField(default=datetime.now,verbose_name=u"创建时间")
    content = MDTextField(verbose_name=u"内容")
    read_count = models.IntegerField(default=0, verbose_name=u"阅读数")
    favorite = models.IntegerField(default=0, verbose_name=u'收藏数')
    username = models.CharField(max_length=20, verbose_name=u"作者", null=True)
    describe = models.CharField(max_length=2500, null=True, verbose_name=u"简介")

    cover = models.ImageField(upload_to="blog/image/%Y/%m", default="image/default.png", max_length=200, null=True, verbose_name=u"封面")

    category = models.ForeignKey(CategoryModel,verbose_name=u"文章分类",on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'文章信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title




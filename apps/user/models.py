import time
from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser


# 用户信息
class UserInformationModel(AbstractUser):

    nike_name = models.CharField(max_length=50,verbose_name=u"昵称",default='')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="female")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=200, null=True)
    describe = models.CharField(max_length=500,default=' ',verbose_name=u'个性签名')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


# 验证码
class EmailVerificationModel(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=200, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, choices=(("register", u'注册'), ("forget", u'密码找回')))
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


# 用户收藏
class UserCollectionMode(models.Model):

    '''
    # 当在用户收藏表中出现时，收藏数+1
    # 用书收藏表中消失时，收藏数-1
    '''

    username = models.CharField(max_length=20,verbose_name=u"用户名",null=True)
    title = models.CharField(max_length=200, verbose_name=u"标题", null=True)
    author = models.CharField(max_length=20,verbose_name=u"作者",null=True)
    coll_time = models.DateField(default=datetime.now, verbose_name=u"收藏时间")
    content_id = models.IntegerField(verbose_name=u"文章id",null=True)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username
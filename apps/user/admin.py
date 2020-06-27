from django.contrib import admin

from .models import *


class UserInformationAdmin(admin.ModelAdmin):

    list_display = ("id",'username', 'email',)

    search_fields = ["id",'username', 'email' ]

    list_filter = ("id",'username', 'email')


admin.site.register(UserInformationModel, UserInformationAdmin)

admin.site.register(UserCollectionMode)

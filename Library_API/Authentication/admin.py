from django.contrib import admin
from .models import CustomUser


class IdShowAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__',)


admin.site.register(CustomUser, IdShowAdmin)

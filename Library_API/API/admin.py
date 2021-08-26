from django.contrib import admin
from .models import Author, Book, Order


class IdShowAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__',)


admin.site.register(Author, IdShowAdmin)
admin.site.register(Book, IdShowAdmin)
admin.site.register(Order)

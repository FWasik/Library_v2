from django.contrib import admin
from .models import Author, Book, Order, Publisher, Genre, Deliverer


class IdShowAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__',)


admin.site.register(Author, IdShowAdmin)
admin.site.register(Book, IdShowAdmin)
admin.site.register(Order)
admin.site.register(Deliverer, IdShowAdmin)
admin.site.register(Genre, IdShowAdmin)
admin.site.register(Publisher, IdShowAdmin)


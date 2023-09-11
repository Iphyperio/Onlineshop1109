from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['title','status']


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['title', 'status']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)


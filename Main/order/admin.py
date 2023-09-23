from django.contrib import admin
from .models import ShopCart

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','price','amount']
    list_filter = ['product','user']

admin.site.register(ShopCart,ShopCartAdmin)
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *
from mptt.admin import DraggableMPTTAdmin

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20

    list_display_links=( 'indented_title',),


class ProductImagesInline(admin.TabularInline):
    model = Images
    extra = 5
    readonly_fields = ('id',)
    #form = MyProductImageInlineForm - если хотите добавить свои поля в Inline


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag','amount']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['title', 'status']
    readonly_fields = ('image_tag',)
    inlines = (ProductImagesInline, ProductVariantsInline)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','product','image_tag','id']
    list_filter = ['product','title']
    readonly_fields = ('image_tag',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['product','subject','rate','status']
    list_filter = ['product','subject','rate','status']
    readonly_fields = ['product','text','ip','user','subject','rate']



class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']





class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','quantity','price','image_tag']


admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Category, DraggableMPTTAdmin,
                    list_display=('tree_actions','indented_title','status'),
                    list_filter=( 'title','status'), prepopulated_fields = {'slug': ('title',)})


admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)


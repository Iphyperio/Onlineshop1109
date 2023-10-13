from .models import *
from modeltranslation.translator import register, TranslationOptions

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title','description')
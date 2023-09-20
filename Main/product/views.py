from django.shortcuts import render, HttpResponse

# Create your views here.
from django.conf import Settings
from .models import *
from home.models import Setting
def index(request):
    return HttpResponse('<h1>Product page </h1>')

def category_products(request,id,slug):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    print(products)
    context = {'setting': setting, 'category': category,
               'products': products }

    return render(request,'product/products.html',context)

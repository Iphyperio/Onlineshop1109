from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import *
from django.contrib import messages
from product.models import Category, Product

from order.models import ShopCart
from users.models import UserProfile

def selectcurrency(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        request.session['currency'] = request.POST['currency']
        userprofile = UserProfile.objects.get(user_id=request.user.id)
        userprofile.currency_id = request.session['currency']
        userprofile.save()
        return HttpResponseRedirect(url)

from django.utils import translation
from django.conf import settings

def selectlanguage(request):
    print('ПУТЬ К ЛОКАЛЯМ', settings.LOCALE_PATHS)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        current_language = translation.get_language()
        lang = request.POST.get('language')
        translation.activate(lang)

        # request.session[LANGUAGE_SESSION_KEY] = lang
        # userprofile = UserProfile.objects.get(user_id=request.user.id)
        # userprofile.currency_id = request.session['currency']
        # userprofile.save()
        response = HttpResponse('')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return HttpResponseRedirect('/'+lang+'/'+url[25:])

def index(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id = request.user.id)
    total = 0
    quantity = 0
    for sc in current_shopcart:
        if sc.variant != None:
            total += sc.variant.price * sc.quantity
        else:
            total += sc.product.price * sc.quantity
        quantity += sc.quantity

    product_slider = Product.objects.order_by('id').all()[:3]
    special_offer = Product.objects.order_by('id').all()[:4]


    context = {'setting': setting, 'category': category,
               'total':int(total), 'quantity':quantity,
               'product_slider': product_slider,
               'special_offer': special_offer,
               }

    return render(request,'home/index.html',context)


def contacts(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    for sc in current_shopcart:
        if sc.variant != None:
            total += sc.variant.price * sc.quantity
        else:
            total += sc.product.price * sc.quantity
        quantity += sc.quantity


    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contactmessage = ContactMessage()
            contactmessage.name = form.cleaned_data['name']
            contactmessage.email = form.cleaned_data['email']
            contactmessage.subject = form.cleaned_data['subject']
            contactmessage.message = form.cleaned_data['message']
            contactmessage.ip = request.META.get('REMOTE_ADDR')
            contactmessage.save()
            messages.success(request,'Сообщение отправлено')
            return HttpResponseRedirect('/contacts/')

    form = ContactForm
    context = {'setting':setting, 'form':form,
               'category':category,
               'total': int(total), 'quantity': quantity,
               }

    return render(request,'home/contacts.html', context)

def aboutus(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    for sc in current_shopcart:
        if sc.variant != None:
            total += sc.variant.price * sc.quantity
        else:
            total += sc.product.price * sc.quantity
        quantity += sc.quantity

    context = {'setting':setting, 'category':category,
               'total': int(total), 'quantity': quantity,
               }

    return render(request,'home/aboutus.html',context)


def search(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0

    for sc in current_shopcart:
        if sc.variant != None:
            total += sc.variant.price * sc.quantity
        else:
            total += sc.product.price * sc.quantity
        quantity += sc.quantity

    if request.method == 'POST':
        query = request.POST['query']
        catid = int(request.POST['cat'][0])
        if catid == 0:
            products = Product.objects.filter(title__icontains=query)
        else:
            products = Product.objects.filter(title__icontains=query,category_id=catid)

    context = {'setting': setting, 'category': category,
               'products': products,'query':query,
               'total': int(total), 'quantity': quantity,
               }
    return render(request,'product/search_results.html',context)


import json

def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        print('Товарчики:',products)
        results = []
        for p in products:
          results.append(p.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    print(data)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
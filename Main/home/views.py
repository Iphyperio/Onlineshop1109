from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import *
from django.contrib import messages
from product.models import Category, Product

def index(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    product_slider = Product.objects.order_by('id').all()[:3]

    context = {'setting': setting, 'category': category,
               'product_slider':product_slider}

    return render(request,'home/index.html',context)


def contacts(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
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
               'category':category}

    return render(request,'home/contacts.html', context)

def aboutus(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()

    context = {'setting':setting, 'category':category}

    return render(request,'home/aboutus.html',context)


def search(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    if request.method == 'POST':
        query = request.POST['query']
        catid = int(request.POST['cat'][0])
        if catid == 0:
            products = Product.objects.filter(title__icontains=query)
        else:
            products = Product.objects.filter(title__icontains=query,category_id=catid)

    context = {'setting': setting, 'category': category,
               'products': products,'query':query}
    return render(request,'product/search_results.html',context)


import json

def search_auto(request):
    print('Сработал Auto_search')
    print(request.headers)
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
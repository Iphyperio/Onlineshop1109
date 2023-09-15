from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.contrib import messages
from product.models import Category

def index(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    context = {'setting': setting, 'category': category}

    return render(request,'home/index.html',context)


def contacts(request):

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
    setting = Setting.objects.filter(status=True).first()
    form = ContactForm
    context = {'setting':setting, 'form':form}

    return render(request,'home/contacts.html', context)

def aboutus(request):
    setting = Setting.objects.filter(status=True).first()
    context = {'setting':setting}

    return render(request,'home/aboutus.html',context)
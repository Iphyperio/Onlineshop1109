from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from order.models import ShopCart
from product.models import Category
from django.contrib.auth.decorators import login_required
from home.models import Setting
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from .models import UserProfile

def index(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               }
    return render(request, 'users/user_profile.html', context)


def login_func(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    total = 0
    quantity = 0
    current_shopcart = None
    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)

        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               }

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        our_user = authenticate(request, username=username, password=password)

        if our_user is not None:
            login(request,our_user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,'Login error. Check username or password')
            return HttpResponseRedirect('/users/login')

    return render(request, 'users/login_form.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_func(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            our_user = authenticate(request, username=username, password=password)
            login(request,our_user)
            data = UserProfile()
            data.user_id = our_user.id
            data.image ='images/users/default.jpg'
            data.save()
            return HttpResponseRedirect('/')

    form = RegistrationForm()
    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'form':form,
               }
    return render(request, 'users/registration_form.html', context)
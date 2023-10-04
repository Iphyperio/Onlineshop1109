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

    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
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
            return HttpResponseRedirect('/user/login')

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


from .forms import ProfileUpdateForm, UserUpdateForm
@login_required(login_url='user/login')
def update_profile(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    user_form = UserUpdateForm(instance = current_user)
    profile_form = ProfileUpdateForm(instance=profile)
    if request.method =='POST':
        user_form = UserUpdateForm(request.POST,instance=current_user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        print(request.FILES, request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
            return HttpResponseRedirect('/user')

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
               'user_form':user_form,
               'profile_form':profile_form,
               }
    return render(request, 'users/update_profile.html', context)


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='user/login')
def update_password(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    form = PasswordChangeForm(current_user,request.POST)
    if request.method =='POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request,'Please correct: <br>'+str(form.errors))
            return HttpResponseRedirect('/user/password/')

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
               'password_form': form,
               }
    return render(request, 'users/update_password.html', context)

from product.models import Product, Comment
from order.models import Order, OrderProduct
def my_orders(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    orders = Order.objects.filter(user_id = current_user.id)
    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
               'orders': orders,
               }
    return render(request, 'users/my_orders.html', context)



def my_order_detail(request,id):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    order = Order.objects.filter(user_id = current_user.id,id=id).first()
    order_products = OrderProduct.objects.filter(order_id = id)


    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
               'order': order,
               'order_products': order_products
               }
    return render(request, 'users/my_order_details.html', context)



def my_products(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    my_ordered_products = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
               'my_products': my_ordered_products,
               }
    return render(request, 'users/my_products.html', context)

def my_comments(request):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    if request.user != 'AnonymousUser':
        current_shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for sc in current_shopcart:
            total += sc.product.price * sc.quantity
            quantity += sc.quantity

    comments = Comment.objects.filter(user_id=current_user.id)
    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total': int(total), 'quantity': quantity,
               'profile': profile,
               'comments': comments,
               }
    return render(request, 'users/my_comments.html', context)







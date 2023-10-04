from django.shortcuts import render, HttpResponse,HttpResponseRedirect

# Create your views here.
from django.conf import Settings
from .models import *
from home.models import Setting
from order.models import ShopCart

def index(request):
    return HttpResponse('<h1>Product page </h1>')







def category_products(request,id,slug):

    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id = request.user.id)
    total = 0
    quantity = 0
    for sc in current_shopcart:
        total += sc.product.price * sc.quantity
        quantity += sc.quantity

    products = Product.objects.filter(category_id=id)

    context = {'setting': setting, 'category': category,
               'products': products,
               'total': int(total), 'quantity': quantity,
               }

    return render(request,'product/products.html',context)

def product_detail(request,id,slug):
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id = request.user.id)
    total = 0
    quantity = 0
    for sc in current_shopcart:
        total += sc.product.price * sc.quantity
        quantity += sc.quantity
    product = Product.objects.filter(id=id)[0]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id)
    context = {'setting': setting, 'category': category,
               'product': product, 'images':images,
               'comments':comments,
               'total': int(total), 'quantity': quantity,

               }

    return render(request,'product/product_detail.html',context)


from .forms import CommentForm
from django.contrib import messages
def add_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        if len(request.POST['rating'])>0 and len(request.POST['subject'])>0 and len(request.POST['text']) > 0:
            data = Comment()
            data.rate = int(request.POST.get('rating'))
            data.subject = request.POST.get('subject')
            data.text = request.POST.get('text')
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            data.user_id = request.user.id
            if not(data.rate is None) and not(data.subject is None) and not(data.text is None):
                data.save()
                messages.success(request,'Your review was created')

    return HttpResponseRedirect(url)


from django.contrib.auth.decorators import login_required
@login_required(login_url='/user/login')
def delete_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    Comment.objects.filter(id=id,user_id = current_user.id).delete()
    messages.success(request,'Your comment was successfully deleted')
    return HttpResponseRedirect(url)
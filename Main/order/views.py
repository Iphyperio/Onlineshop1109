from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import ShopCart
from .forms import ShopCartForm
from django.contrib.auth.decorators import login_required
from home.models import Setting

def index(request):
    return HttpResponse('Страница Order')

@login_required(login_url='/login')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id, user_id=request.user.id)

    if checkproduct: control = 1 #товар в корзине
    else: control = 0            #товар не в корзине

    if request.method == "POST":
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1: #Обновляем корзину
                data = ShopCart.objects.get(product_id=id, user_id=request.user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
                messages.success(request, 'Корзина обновлена')
            else: #добавляем в корзину
                data=ShopCart()
                data.user_id = current_user.id
                data.product_id=id
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request,'Товар добавлен в корзину')
        return HttpResponseRedirect(url)
    else: #если это не РОST запрос
        if control ==1:
            data= ShopCart.objects.get(product_id=id, user_id=request.user.id)
            data.quantity +=1 #если еще раз ткнули добавить тот же товар
            data.save()
            messages.success(request, 'Корзина обновлена')
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.product_id=id
            data.quantity=1 #только 1 товар
            data.save()
            messages.success(request,'Товар добавлен в корзину')
        return HttpResponseRedirect(url)


from product.models import Category, Product
def shopcart(request):
    print('Shopcart сработал !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    current_shopcart = ShopCart.objects.filter(user_id = request.user.id)
    total = 0
    quantity = 0
    for sc in current_shopcart:
        total += sc.product.price * sc.quantity
        quantity += sc.quantity

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total':int(total), 'quantity':quantity,
               }

    return render(request,'order/shopcart.html',context)
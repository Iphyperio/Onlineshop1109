
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import ShopCart, Order, OrderProduct
from .forms import ShopCartForm
from django.contrib.auth.decorators import login_required
from home.models import Setting
from product.models import Category, Product, Variants


def index(request):
    return HttpResponse('Страница Order')

@login_required(login_url='/user/login')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Product.objects.filter(id = id).first()

    if product.variant != 'None':
        variantid = request.POST.get('cd-dropdown')
        if variantid == None:#пересылка на страницу товара
            return HttpResponseRedirect(f'/category/product/{id}/{product.slug}/')
        if variantid == '0':
            messages.warning(request, 'Выберите конфигурацию!')
            return HttpResponseRedirect(url)
        variantid = int(variantid)
        #Проверяем что в корзине уже был такой вариант товара
        checkvariant = ShopCart.objects.filter(product_id=id,variant_id=variantid,
                                               user_id=current_user.id)
        if checkvariant:
            control = 1 #если был то 1
        else:
            control = 0 # если нет - то 0
    else: #товар не имеет конфигураций
        checkproduct = ShopCart.objects.filter(product_id=id, user_id=request.user.id)
        if checkproduct:
            print('Есть товар')
            control = 1  # товар в корзине
        else:
            control = 0  # товар не в корзине


    if request.method == "POST":
        form = ShopCartForm(request.POST)
        if form.is_valid():
            # !!!! поправил ключ для вытаскивания ID из запроса
            variantid = request.POST.get('cd-dropdown')
            print('РОСТ запрос', variantid)
            if control == 1: #Обновляем корзину
                if product.variant == 'None': #у товара нет конфигураций
                    data = ShopCart.objects.get(product_id=id, user_id=request.user.id)
                else:#у товара есть конфигурации
                    #!!!! поправил Variant_id = variantid
                    data = ShopCart.objects.get(variant_id=variantid, product_id=id, user_id=request.user.id)
                    print('Конфигурации:',data)

                data.quantity += form.cleaned_data['quantity']
                data.save()
                messages.success(request, 'Корзина обновлена')
            else: #добавляем в корзину
                data=ShopCart()
                data.user_id = current_user.id
                data.product_id=id
                print('ID ВАРИАНА!!!!!!!', variantid)
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request,'Товар добавлен в корзину')
        return HttpResponseRedirect(url)
    else: #если это не РОST запрос
        if product.variant == 'None': #если нет конфигураций - добавляем 1 штуку
            if control ==1:
                data= ShopCart.objects.get(product_id=id, user_id=request.user.id)
                data.quantity +=1 #если еще раз ткнули добавить тот же товар
                data.save()
                messages.success(request, 'Корзина обновлена')
            else:
                data=ShopCart()
                data.user_id=current_user.id
                data.product_id=id
                data.variant_id = None
                data.quantity=1 #только 1 товар
                data.save()
                messages.success(request,'Товар добавлен в корзину')
        else: #если конфигурации есть - делаем переадресацию на страницу товара
            return HttpResponseRedirect(f'/category/product/{id}/{product.slug}/')

        return HttpResponseRedirect(url)



def shopcart(request):
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

    context = {'setting': setting, 'category': category,
               'shopcart': current_shopcart,
               'total':int(total), 'quantity':quantity,
               }

    return render(request,'order/shopcart.html',context)


#from user.models import UserProfile
from django.utils.crypto import get_random_string
from django.contrib import messages
from  .forms import OrderForm
from .models import ShopCart, Order, OrderProduct
from users.models import UserProfile
def checkout(request):
    current_user = request.user
    setting = Setting.objects.filter(status=True).first()
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    quantity = 0
    for sc in shopcart:
        if sc.variant != None:
            total += sc.variant.price * sc.quantity
        else:
            total += sc.product.price * sc.quantity
        quantity += sc.quantity

    profile = UserProfile.objects.get(user_id=current_user.id)


    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #Не забудьте проверить информацию о кредитной карте пользователя и возможности оплаты
            #на реальном проекте
            #Получаем информацию из формы пользователя
            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            #случайная строка из 5 символов - код заказа
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            #Далее - получаем информацию из корзины и перебираем товары
            #добавляем их в заказ, уменьшаем остатки на складе
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for s in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # ID заказа (сформировали случайно)
                detail.product_id = s.product_id #ID Товара
                detail.user_id = current_user.id #ID пользователя
                detail.quantity = s.quantity #количество
                detail.variant = s.variant
                if s.variant_id != None:
                    detail.price = s.variant.price #цена
                else:
                    detail.price = s.product.price  # цена
                detail.amount = s.amount #итоговая сумма по этому товару

                detail.save()
                if s.variant_id != None:
                    variants = Variants.objects.filter(id=s.variant_id).first()
                    variants.quantity -= s.quantity
                    variants.save()
                else:
                    product = Product.objects.get(id=s.product_id)
                    product.amount -= s.quantity  # Уменьшаем количество товара
                    product.save() #сохраняем заказ в БД

            # очищаем корзину после формирования заказа - удаляем из БД
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0 #количество товаров в корзине - обнуляем
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'order/order_complete.html', {'ordercode': ordercode,
                                                                 'category': category,
                                                                 'setting': setting,
                                                                 })
        else: #на всякий случай вывод ошибок при валидации
            print('ОШИБКИ', form.errors)
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/checkout/")
    else:
        print('НЕ ПОСТ ЗАПРОС !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    context = {'category': category,
               'shopcart': shopcart,
               'setting': setting,
               'profile':profile,
               'total': int(total),
               'quantity': quantity,
               }
    return render(request, 'order/checkout.html', context)




from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Variants

class ShopCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null = True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null = True)
    quantity = models.IntegerField()
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null = True, blank=True)

    @property
    def price(self):
        if self.variant != None:
            return self.variant.price
        else:
            return self.product.price

    @property
    def amount(self):
        return self.quantity * self.price

    @property
    def product_info(self):
        if self.variant == None:
            return self.product.title
        else:
            return self.variant

    def __str__(self):
        return f'<Shopcart. User: {self.user}, product:{self.product}:{self.quantity}>'


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False )
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.CharField(blank=True, max_length=80)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    #Относится к модели Order
    def __str__(self):
        return self.user.first_name



class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, null = True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


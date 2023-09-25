
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.index, name='order_index'),
    path('addtoshopcart/<int:id>/', views.addtoshopcart, name='addtoshopcart'),
    path('shopcart/', views.shopcart, name='shopcart'),

]

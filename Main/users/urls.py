from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.index, name='user_profile'),
    path('login/',views.login_func,name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('register/', views.register_func, name='register'),
    path('profile/',views.update_profile,name='update_profile'),
    path('password/', views.update_password, name='update_password'),
    path('orders/', views.my_orders, name='my_orders'),
    path('myorderdetail/<int:id>/', views.my_order_detail, name='my_order_detail'),
    path('ordered_products/', views.my_products, name='my_products'),
    path('comments/', views.my_comments, name='my_comments'),
]

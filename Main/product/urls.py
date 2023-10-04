
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.index, name='product_index'),
    path('<int:id>/<slug:slug>/',views.category_products,name='category_products'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/add_comment/<int:id>/', views.add_comment, name='add_comment'),
    path('product/delete_comment/<int:id>/',views.delete_comment,name='delete_comment')
]

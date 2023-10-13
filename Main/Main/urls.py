"""
URL configuration for Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from home import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('selectlanguage/', views.selectlanguage, name='selectlanguage'),
    path('i18n/', include('django.conf.urls.i18n')),
    ]
urlpatterns+=i18n_patterns(
    path('', include('home.urls')),
    path('currencies/', include('currencies.urls')),
    path('slectcurrency/',views.selectcurrency, name='selectcurrency'),
    path('category/',include('product.urls')),
    path('order/', include('order.urls')),
    path('user/', include('users.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', views.search, name='search'),
    path('search/search_auto/', views.search_auto, name='search_auto'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
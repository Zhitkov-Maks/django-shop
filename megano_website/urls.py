"""megano_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.staticfiles.views import serve
from django.views.static import serve as media_serve
from django.conf import settings

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('app_megano.urls')),
    path('user/', include('app_users.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('orders.urls')),
]

if not settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', serve, {'insecure': True}))
    urlpatterns.append(path('media/<path:path>', media_serve, {'document_root': settings.MEDIA_ROOT}))

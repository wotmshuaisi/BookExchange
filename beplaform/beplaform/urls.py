from django.http import HttpResponse
"""beplaform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from django.shortcuts import render


def index(request, path=''):
    return render(request, settings.HOMEFILE_PATH)


urlpatterns = [
    path('admin/', admin.site.urls),

    # rest
    path('api-auth/', include('rest_framework.urls')),

    # api
    url(r'^api/', include('api.urls'), name='api'),

    # angular routes
    url(r'^$', index, name='index'),
    url(r'^post/?', index, name='index'),
    url(r'^detail/?', index, name='index'),
    url(r'^register/?', index, name='index'),
    url(r'^login/?', index, name='index'),
    *static('/', document_root=settings.STATIC_PATH),
]

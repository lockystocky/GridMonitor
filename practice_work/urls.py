"""practice_work URL Configuration

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
from django.urls import path

from LdapScheduler import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from practice_work import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'interface/(?P<name>[\w.]+)', views.interface),
    url(r'interfaceinfo/(?P<name>[\w.]+)', views.interfaceinfo),
    url(r'computingshare/(?P<name>[\w._:\d]+)', views.computingshare),
    url(r'environment/(?P<name>[\w._:\d]+)', views.environment),
    path('', views.Home.as_view())
]


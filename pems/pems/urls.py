"""pems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include
from django.contrib import admin

from django.template import loader

from django.http import HttpResponse

# Aqui pones los enpoints de la app web generales. Depues llama individualmente a solar, user, ML...

def index(request):
    template = loader.get_template('index/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^solar/', include('solar.urls')),
    url(r'', index),
]

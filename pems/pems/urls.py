from django.conf.urls import url
from django.urls import include
from django.contrib import admin

from django.template import loader

from django.http import HttpResponse

# Aqui pones los enpoints de la app web generales. Depues llama individualmente a solar, user, ML...

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^solar/', include('solar.urls')),
    url(r'', index),
]

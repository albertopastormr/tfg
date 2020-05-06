from django.conf.urls import url
from django.urls import include
from django.contrib import admin

from django.template import loader

from django.http import HttpResponse

# Aqui pones los enpoints de la app web generales. Depues llama individualmente a solar, user, ML...

def control_endpoint_template(request, url_template):
    template = loader.get_template(url_template)
    context = {}
    return HttpResponse(template.render(context, request))

def index(request):
    return control_endpoint_template(request = request, url_template='index.html')

def contact(request):
    return control_endpoint_template(request = request, url_template='general/contact.html')

def about_us(request):
    return control_endpoint_template(request = request, url_template='general/about_us.html')

def repository(request):
    return control_endpoint_template(request = request, url_template='general/repository.html')

def contribute(request):
    return control_endpoint_template(request = request, url_template='general/contribute.html')

def support(request):
    return control_endpoint_template(request = request, url_template='general/support.html')

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^solar/', include('solar.urls'), name='solar'),
    url(r'^contact/', contact, name='contact'),
    url(r'^about_us/', about_us, name='about_us'),
    url(r'^repository/', repository, name='repository'),
    url(r'^contribute/', contribute, name='contribute'),
    url(r'^support/', support, name='support'),
    url(r'^admin/', admin.site.urls),
    url(r'', index, name='index')
]

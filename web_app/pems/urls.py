from django.conf.urls import url
from django.urls import include
from django.contrib import admin
from django.template import loader
from django.http import HttpResponse


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


def request_access(request):
    return control_endpoint_template(request = request, url_template='registration/register.html')


def bad_request(request):
    return control_endpoint_template(request = request, url_template='404.html')


def server_error(request):
    return control_endpoint_template(request = request, url_template='500.html')


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^solar/', include('solar.urls'), name='solar'),
    url(r'^monitoring/', include('monitoring.urls'), name='monitoring'),
    url(r'^optimization/', include('optimization.urls'), name='optimization'),
    url(r'^contact/', contact, name='contact'),
    url(r'^about_us/', about_us, name='about_us'),
    url(r'^repository/', repository, name='repository'),
    url(r'^contribute/', contribute, name='contribute'),
    url(r'^support/', support, name='support'),
    url(r'^register/', request_access, name='register'),
    url(r'^404/', bad_request, name='404'),
    url(r'^500/', server_error, name='500'),
    url(r'^admin/', admin.site.urls),
    url(r'', index, name='index')
]

from django.urls import path
from django.urls import include

from . import views

# URL especifico de solar para redireccionar a sus difernetes informes
urlpatterns = [
    # ex: /solar
    path('', views.solar_menu),
    path('solar_report/', views.solar_report, name="solar_report"),
]


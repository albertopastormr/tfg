from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.monitoring_menu),
    path('monitoring/', views.monitoring, name="monitoring_report"),
]

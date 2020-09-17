from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.optimization_menu),
    path('modelo/', views.optimization, name="optimization_report"),
]

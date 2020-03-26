from django.urls import path

from . import views

urlpatterns = [
    # ex: /solar
    path('', views.home)
]

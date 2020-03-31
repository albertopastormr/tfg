from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    # ex: /solar
    path('', views.solar),
]


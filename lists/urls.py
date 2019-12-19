# coding: utf-8
from __future__ import unicode_literals

from django.urls import path
from . import views

__all__ = ["urlpatterns"]

app_name = "lists"

urlpatterns = [
    path('', views.home_page, name='home-page'),
]

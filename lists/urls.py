# coding: utf-8
from __future__ import unicode_literals

from django.urls import path
from . import views

__all__ = ["urlpatterns"]

app_name = "lists"

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('<int:list_id>/',views.view_list, name='view_list'),
    path('new',views.new_list, name='new_list'),
    path('<int:list_id>/add_item',views.add_item,name='add_item'),
]

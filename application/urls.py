from django.contrib import admin
from django.urls import path, include, re_path
from application import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.base_view),
    path('item/', views.index),
    path('category/<customer>/', views.category_view),
]

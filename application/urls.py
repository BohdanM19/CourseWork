from django.contrib import admin
from django.urls import path, include, re_path
from application import views
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', views.base_view),
    path('item/<slug_item>/', views.item_view, name='item_detail'),
    path('category/<customer_slug>/<item_category>', views.category_items_view, name='category_items_detail'),
    path('category/<customer_slug>/', views.category_view, name='category_detail'),
    path('add-to-cart/<item_slug>', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<item_slug>', views.remove_from_cart_view, name='remove_from_cart'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('cart/', cart_view, name='cart'),
]

from django.contrib import admin
from django.urls import path, include, re_path
from application import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
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
    path('account/', account_view, name='account'),
    path('order/', order_create_view, name='create_order'),
    path('thank-you/', TemplateView.as_view(template_name='thank_you.html')),
    path('confirm-order/', make_order_view, name='confirm_order'),

]

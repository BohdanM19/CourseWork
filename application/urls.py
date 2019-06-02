from django.urls import path, reverse_lazy
from application import views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', views.base_view, name='base'),
    path('item/<slug_item>/', views.item_view, name='item_detail'),
    path('category/<customer_slug>/<item_category>', views.category_items_view, name='category_items_detail'),
    path('category/<customer_slug>/', views.category_view, name='category_detail'),
    path('add-to-cart/<item_slug>', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<item_slug>', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/', cart_view, name='cart'),
    path('account/', account_view, name='account'),
    path('registration/', registration_view, name='registration'),
    path('order/', order_create_view, name='create_order'),
    path('thank-you/', TemplateView.as_view(template_name='thank_you.html')),
    path('confirm-order/', make_order_view, name='confirm_order'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    path('login/', login_view, name='login'),

]


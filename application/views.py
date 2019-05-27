from django.shortcuts import render
from .models import *
from django.contrib.auth.views import LoginView
import random
from django.http import HttpResponseRedirect


def get_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def rand_items(n):
    my_ids = Item.objects.values_list('id', flat=True)
    my_ids = list(my_ids)

    rand_ids = random.sample(my_ids, n)
    return rand_ids


def base_view(request):
    cart = get_cart(request)
    cust_categories = CustomerCategory.objects.all()
    items = Item.objects.filter(id__in=rand_items(3))
    context = {
        'Customers': cust_categories,
        'Items': items,
        'cart': cart,
    }
    return render(request, "base.html", context)


def category_view(request, customer_slug):
    cust_categories = CustomerCategory.objects.all()
    required_customer = CustomerCategory.objects.get(slug=customer_slug)
    required_cust_category = Category.objects.filter(customer_category_id=required_customer.id)

    cart = get_cart(request)
    context = {
        'customers_cat': required_cust_category,
        'Customers': cust_categories,
        'cart': cart,
    }
    return render(request, "category.html", context)


def category_items_view(request, customer_slug, item_category):
    cust_categories = CustomerCategory.objects.all()
    required_items = Category.objects.get(slug=item_category)
    items = Item.objects.filter(category_id=required_items.id)
    name = CustomerCategory.objects.get(slug=customer_slug)
    cart = get_cart(request)
    context = {
        'Customers': cust_categories,
        'Items': items,
        'cart': cart,
        'Name': name,
    }
    return render(request, "category_items.html", context)


class UserLoginView(LoginView):
    template_name = 'login.html'


def cart_view(request):
    cart = get_cart(request)
    cust_categories = CustomerCategory.objects.all()
    context = {
        'cart': cart,
        'Customers': cust_categories,
    }
    return render(request, 'cart.html', context)


def item_view(request, slug_item):
    cart = get_cart(request)
    cust_categories = CustomerCategory.objects.all()
    item = Item.objects.get(slug=slug_item)
    context = {
        'Customers': cust_categories,
        'cart': cart,
        'Item': item,
    }
    return render(request, 'item.html', context)


def add_to_cart_view(request, item_slug):
    product = Item.objects.get(slug=item_slug)
    cart_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    cart = get_cart(request)
    if cart_item not in cart.items.all():
        cart.items.add(cart_item)
        cart.save()

    return HttpResponseRedirect("/cart/")


def remove_from_cart_view(request, item_slug):
    product = Item.objects.get(slug=item_slug)
    cart = get_cart(request)
    for cart_item in cart.items.all():
        if cart_item.product == product:
            cart.items.remove(cart_item)
            cart.save()
            return HttpResponseRedirect("/cart/")

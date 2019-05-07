from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from .forms import UserForm
from django.http import HttpResponseNotFound
from django.http import HttpResponse
import bcrypt


def index(request):
    return render(request, "item.html", )


def base_view(request):
    cust_categories = CustomerCategory.objects.all()
    items = Item.objects.all()
    context = {
        'Customers': cust_categories,
        'Items': items,
    }
    return render(request, "base.html", context)


def category_view(request,customer):
    cust_categories = CustomerCategory.objects.all()
    items = Item.objects.all()
    context = {
        'Customers': cust_categories,
        'Items': items,
    }
    return render(request, "category.html",context)

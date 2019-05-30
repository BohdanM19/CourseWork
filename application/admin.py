from django.contrib import admin
from application.models import *

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(CustomerCategory)
admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)

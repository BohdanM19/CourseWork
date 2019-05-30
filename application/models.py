from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class CustomerCategory(models.Model):
    CUST_CATEGORY = (
        ('Мужчинам', "Мужчины"),
        ('Женщинам', "Женщины"),
        ('Мальчикам', "Мальчики"),
        ('Девочкам', "Девочки"),
    )
    name = models.CharField(max_length=15, choices=CUST_CATEGORY, unique=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'customer_slug': self.slug})


def pre_save_customer_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(instance.name, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_customer_category_slug, sender=CustomerCategory)


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return '{0}/{1}'.format(instance.slug, filename)


class Category(models.Model):
    title = models.CharField(max_length=100)
    name_in_admin = models.CharField(max_length=100, default='')
    slug = models.SlugField(blank=True)
    customer_category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE, default='')
    image = models.ImageField(upload_to=image_folder)

    def __str__(self):
        return self.name_in_admin


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        cust_slug = CustomerCategory.objects.get(id=instance.customer_category_id)
        cust_slug = cust_slug.slug
        slug = slugify(translit(instance.title + "-" + cust_slug, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class ItemManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ItemManager, self).get_queryset().filter(available=True)


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    size = models.CharField(max_length=100)
    material = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(default='')
    image = models.ImageField(upload_to=image_folder)
    available = models.BooleanField(default=True)
    objects = ItemManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'slug_item': self.slug})


def pre_save_item_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(instance.name, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_item_slug, sender=Item)


class CartItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return "Cart item for product {0}".format(self.product.name)


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True, )
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)


ORDER_STATUS_CHOICES = (
    ("Принят в обработку", "Принят в обработку"),
    ("Выполняеться", "Выполняеться"),
    ("Оплачен", "Оплачен")
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), ("Доставка", "Доставка")),
                                   default='Самовывоз')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Принят в обработку')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return "Заказ №{}".format(str(self.id))

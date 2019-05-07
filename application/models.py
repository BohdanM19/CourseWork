from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from transliterate import translit


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
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100)
    name_in_admin = models.CharField(max_length=100, default='')
    slug = models.SlugField(blank=True)
    customer_category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.name_in_admin


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        cust_slug = CustomerCategory.objects.get(id=instance.customer_category_id)
        cust_slug = cust_slug.slug
        slug = slugify(translit(instance.title + "-" + cust_slug, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return '{0}/{1}'.format(instance.slug, filename)


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

    def __str__(self):
        return self.name


def pre_save_item_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(instance.name, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_item_slug, sender=Item)

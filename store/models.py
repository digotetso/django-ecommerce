from ast import arg
from re import U
from unicodedata import category
from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/products')
    price = models.IntegerField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def get_url(self):
        # product_detail --> url name
        # self.category.slug, self.slug ---> '<slug:category_slug>/<slug:product_slug>'
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.product_name

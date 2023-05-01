from ast import arg
from pyexpat import model
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
    # on_delete --> when Category is deleted all product using this category will be deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        # product_detail --> url name
        # self.category.slug, self.slug ---> '<slug:category_slug>/<slug:product_slug>'
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.product_name


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

# manage and should able to separate different variantions: color and size


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    # many-to-One
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now=True)

    # use variation manager:
    objects = VariationManager()

    def __str__(self):
        return self.variation_value

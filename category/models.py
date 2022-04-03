from distutils.command.upload import upload
from unicodedata import category
from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    desciption = models.TextField(max_length=200, unique=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    # define plural name to by used @admin
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # instaed of an object, this category_name will be used  as a display name
    def __str__(self) -> str:
        return self.category_name

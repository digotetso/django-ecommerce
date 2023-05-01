from django.contrib import admin

from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)} #auto populated in categories slug
    list_display = ('category_name', 'slug', 'cat_image')


admin.site.register(Category, CategoryAdmin)

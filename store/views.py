from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,  get_object_or_404

from store.models import Product
from category.models import Category


# Create your views here.


def store(request, category_slug=None):
    print(f'some slugs: {category_slug}')

    categories = None
    products = None

    categories = Category.objects.all()

    if category_slug != None:
        # DISPLAY products by category

        # get objects from 'Category' Model, where slug='category_slug'
        category_ = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=category_, is_available=True)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(
            is_available=True)  # only return available products
    context = {
        'products': products,
        'categories': categories
    }

    print(products)

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        # since  'category' a foreign key --> category__slug
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)

    except Exception as e:
        raise e

    context = {
        'single_product':  single_product,

    }

    return render(request, 'store/product-detail.html', context)

from ast import keyword
from itertools import product
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,  get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from cart.models import CartItem
from django.db.models import Q

from store.models import Product
from category.models import Category
from cart.views import _cart_id
from cart.models import CartItem

# Create your views here.

# DISPLAY ALL PRODUCTS ON STORE PAGE OR BY CATEGORY
def store(request, category_slug=None):
    # category_slug ---> passed from url
    print(f'some slugs: {category_slug}')

    categories = None
    products = None

    categories = Category.objects.all()

    if category_slug != None:
        # Get  products by category from db

        # get objects from 'Category' Model, where slug='category_slug'
        category_ = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=category_, is_available=True)
        paginator = Paginator(products, 3)  # display 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = paged_products.count

    else:
        # TO get all available products from DB
        products = Product.objects.all().filter(
            is_available=True).order_by('id')  # only return available products
        paginator = Paginator(products, 2)  # display 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = paged_products.count  # ???
    context = {
        'products': paged_products,
        'categories': categories,
        'product_count': product_count
    }

    print(f'paged:  {paged_products}')

    return render(request, 'store/store.html', context)

# DISPLAY DETAILED PRODUCT PAGE, WHEN CLICKING ON A PRODUCT CARD
def product_detail(request, category_slug, product_slug):

    try:
        # since  'category' a foreign key --> category__slug
        # for url; "/store/t-shirt/great-tshirt"
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)  # e.g /shoes/sneaker ---> category_slug/product_slug
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
    except Exception as e:
        raise e

    print(f'This is a sngle product: {single_product}')

    print(f'variations: {single_product.variation_set.all()}')
    context = {
        'single_product':  single_product,
        'in_cart': in_cart
    }

    return render(request, 'store/product-detail.html', context)

# Implement search functionality...

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)

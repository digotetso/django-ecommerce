from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product

# Create your views here.


def store(request):

    products = Product.objects.all().filter(
        is_available=True)  # only return available products
    context = {'products': products}

    print(products)

    return render(request, 'store/store.html', context)

from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product
from pprint import pprint


# Create your views here.


def home(request):
    print(f'------------------------------------------------------------------------')
    pprint(f'req.session: {request.session.session_key}')
    print(f'------------------------------------------------------------------------')
    print(f'Next...')
    print(f'------------------------------------------------------------------------')
    pprint(f'{request.get_port()}')
    print(f'------------------------------------------------------------------------')

    products = Product.objects.all().filter(
        is_available=True)  # only return available products
    context = {'products': products}

    print(products)

    return render(request, 'home.html', context)

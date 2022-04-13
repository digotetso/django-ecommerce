from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product
from .models import Cart, CartItem

# Create your views here.


# get the current session_id --> dee heck the browser to see session_id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        # 1 create a session
        request.session.create()

    return cart


def add_cart(request, product_id):

    # for variation
    color = request.GET['color']
    size = request.GET['size']

    print(color, size)
    product = Product.objects.get(id=product_id)

    # 1 GET or CREATE a cart
    try:
        # after we get the seesion_id, use it the get the cart
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        # 2 create a cart with a session ID
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    # 2 GET a product from CART  or ADD a product to a CART --> cartItem
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()

   # create a new cart if it doesn't exist
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return redirect('cart')  # Goto cart page


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, quantity=0, total=0, cart_items=None):
    # GET cart_item info
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        # get price, total, quantity

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (0.14 * total)
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': (tax + total),
        'tax': tax
    }

    return render(request, 'store/cart.html', context)

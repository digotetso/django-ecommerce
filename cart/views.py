from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product, Variation
from .models import Cart, CartItem

# 1 Create your views here.
# 2 get the current session_id --> dee heck the browser to see session_id


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        # 1 create a session
        request.session.create()

    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if(request.method == 'POST'):
        # for variation
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                # variation_category__iexact='color', variation_value__iexact='red'
                # iexact ---> Case-insensitive exact match
                variation = Variation.objects.get(product=product,
                                                  variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                print(f' my variation: {variation}')
            except:
                pass

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

    # check if cartItems  exists:
    is_cart_item_exists = CartItem.objects.filter(
        product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        # check existing variations in db
        # check the current variation --> product_variation
        # check item_id in db

        # **** if the current variation in the existing variations in db, increase the quantity of cartItem§
        ####################################
        # Group CartItems
        ####################################
        exit_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            exit_var_list.append(list(existing_variation))
            id.append(item.id)

            print(f'Product vars: {product_variation}')
            print(f'exit_var_list {exit_var_list}')

            if product_variation in exit_var_list:
                # inrease the cart quantity
                index = exit_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)

                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

   # create a new cart if it doesn't exist
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')  # Goto cart page --> path('', views.cart, name='cart')


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
    return redirect('cart')  # --> path('', views.cart, name='cart')


# triggered by : path('', views.cart, name='cart')
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
        'tax': tax,
    }

    return render(request, 'store/cart.html', context)

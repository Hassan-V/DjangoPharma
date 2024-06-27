from django import template
from django.shortcuts import get_object_or_404
from central.models import Product, Cart, CartItem

register = template.Library()

@register.simple_tag(takes_context=True)
def add_to_cart(context, product_id, quantity=1):
    request = context['request']
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user, defaults={'session_key': request.session.session_key})
        cart_id = user_cart.id
    elif cart_id:
        user_cart, created = Cart.objects.get_or_create(id=cart_id, defaults={'session_key': request.session.session_key})
    else:
        user_cart = Cart.objects.create(session_key=request.session.session_key)
        request.session['cart_id'] = user_cart.id

    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product, defaults={'quantity': quantity})
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return ""

@register.simple_tag(takes_context=True)
def remove_from_cart(context, product_id):
    request = context['request']
    cart_id = request.session.get('cart_id')
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(id=cart_id).first()

    if cart:
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    return ""

@register.simple_tag(takes_context=True)
def update_cart_item_quantity(context, product_id, quantity):
    request = context['request']
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        cart, created = Cart.objects.get_or_create(id=cart_id, defaults={'session_key': request.session.session_key})

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.quantity = quantity
        cart_item.save()

    return ""

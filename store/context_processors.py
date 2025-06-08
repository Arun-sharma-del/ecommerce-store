def cart(request):
    from .cart import Cart
    return {'cart': Cart(request)}
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
     from .models import Product
     product_ids = self.cart.keys()
     products = Product.objects.filter(id__in=product_ids)
     cart = self.cart.copy()  # copy from session

     for product in products:
        cart_item = cart[str(product.id)].copy()  # create a copy to avoid modifying session
        cart_item['product'] = product
        cart_item['price'] = float(cart_item['price'])
        cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
        yield cart_item
        

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def update_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
          if quantity < 1:
            del self.cart[product_id]
          else:
              self.cart[product_id]['quantity'] = quantity
          self.save()
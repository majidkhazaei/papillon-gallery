from products.models import Product

CART_SESSION_ID = 'user_cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID, None)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for key, item in cart.items():
            product_id, size = key.split('-')
            product = Product.objects.get(id=product_id)
            item['product'] = product
            item['size'] = size
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity, size):
        variant = product.variants.filter(size=size).first()
        if not variant:
            raise ValueError("سایز انتخاب شده نامعتبر است")

        key = f"{product.id}-{size}"
        if key not in self.cart:
            self.cart[key] = {
                'product_id': str(product.id),
                'size': size,
                'quantity': 0,
                'price': str(variant.price)
            }
        self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, product):
        keys_to_delete = [key for key in self.cart.keys() if key.startswith(f"{product.id}-")]
        for key in keys_to_delete:
            del self.cart[key]
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
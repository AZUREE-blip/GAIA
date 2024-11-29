import sqlite3
from currency import convert_price

class Cart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, product_id, quantity):
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity

    def remove_from_cart(self, product_id):
        if product_id in self.items:
            del self.items[product_id]  # Remove item from cart

    def get_cart_items(self, currency="SEK"):
        conn = sqlite3.connect('fashion_brand.db')
        cursor = conn.cursor()
        cart_items = []
        for product_id, quantity in self.items.items():
            cursor.execute('SELECT name, price FROM products WHERE id = ?', (product_id,))
            product = cursor.fetchone()
            if product:
                name, price_sek = product
                price_converted = convert_price(price_sek, currency)
                cart_items.append((product_id, name, quantity, price_converted))
        conn.close()
        return cart_items

    def get_cart_total(self, currency="SEK"):
        conn = sqlite3.connect('fashion_brand.db')
        cursor = conn.cursor()
        total = 0.0
        for product_id, quantity in self.items.items():
            cursor.execute('SELECT price FROM products WHERE id = ?', (product_id,))
            price_sek = cursor.fetchone()[0]
            price_converted = convert_price(price_sek, currency)
            total += price_converted * quantity
        conn.close()
        return total



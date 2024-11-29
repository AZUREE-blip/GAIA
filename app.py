from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import sqlite3
import requests
from cart import Cart  # Ensure this module is implemented correctly
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Use a securely stored key
CORS(app)
cart = Cart()

def get_db_connection():
    """Helper function to get a database connection."""
    return sqlite3.connect('fashion_brand.db')

# Redirect the home route to the landing page
@app.route('/')
def home():
    return redirect(url_for('landing'))

# Route for the landing page
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Route for the gallery page to display products based on selected category
@app.route('/gallery')
def gallery():
    category = request.args.get('category', '')  # Get the category from the URL query parameter
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'SELECT id, name, price, image_url FROM products'
        params = []
        if category:
            query += ' WHERE category = ?'
            params.append(category)
        cursor.execute(query, params)
        items = [
            {"id": row[0], "name": row[1], "price": row[2], "image_url": row[3]}
            for row in cursor.fetchall()
        ]
    currency = session.get("currency", "SEK")
    return render_template('gallery.html', items=items, category=category, currency=currency)

# Route for removing an item from the cart
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart.remove_from_cart(product_id)
    return redirect(url_for('view_cart'))

# Route for individual item detail page
@app.route('/item/<int:item_id>')
def view_item(item_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price, image_url FROM products WHERE id = ?', (item_id,))
        row = cursor.fetchone()

    if row:
        item = {"id": row[0], "name": row[1], "price": row[2], "image_url": row[3]}
        currency = session.get("currency", "SEK")
        return render_template('item.html', item=item, currency=currency)
    else:
        return "Item not found", 404

# Route to handle setting the currency based on user selection
@app.route('/set_currency', methods=['POST'])
def set_currency():
    data = request.get_json()
    currency = data.get("currency")
    if currency:
        session["currency"] = currency
    return jsonify(success=True)

# Route to handle adding items to the cart using item_id
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))

    if item_id:
        cart.add_to_cart(int(item_id), quantity)

    return redirect(url_for('view_cart'))

# Route to display the cart contents
@app.route('/cart')
def view_cart():
    currency = session.get("currency", "SEK")
    cart_items = cart.get_cart_items(currency=currency)
    total = cart.get_cart_total(currency=currency)
    return render_template('cart.html', cart_items=cart_items, total=total, currency=currency)

# Route for the checkout page
@app.route('/checkout_fill')
def checkout_fill():
    cart_items = cart.get_cart_items(currency=session.get("currency", "SEK"))
    total = cart.get_cart_total(currency=session.get("currency", "SEK"))
    currency = session.get("currency", "SEK")
    paypal_client_id = os.getenv("PAYPAL_CLIENT_ID")  # Load the PayPal client ID from environment variables
    return render_template('checkout_fill.html', cart_items=cart_items, total=total, currency=currency, paypal_client_id=paypal_client_id)

# Route to process the order
@app.route('/process_order', methods=['POST'])
def process_order():
    name = request.form.get('name')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    cart_items = cart.get_cart_items(currency=session.get("currency", "SEK"))
    total = cart.get_cart_total(currency=session.get("currency", "SEK"))

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (name, address, email, phone, items, total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, address, email, phone, str(cart_items), total))
        conn.commit()

    # Clear the cart after processing the order
    cart.clear_cart()

    return render_template('checkout.html', message="Thank you for your order!")

if __name__ == '__main__':
    app.run(debug=True)


















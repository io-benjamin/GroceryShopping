from flask import Flask, jsonify, request, abort 
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = "postgres://product_1uus_user:P4R1CX1EW9zkxmM1cX4irZJZb65buMz7@dpg-ck86vlo8elhc73ebc670-a/product_1uus"

shopping_cart = {}

def get_product_details(product_id):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    return None 

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id not in shopping_cart:
        return jsonify({"error": "Cart not found"}), 404
    cart = shopping_cart[user_id]
    return jsonify(cart)

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.json
    if 'quantity' not in data: 
        return jsonify({"error": "Quantity not specified"}), 400
    
    product = get_product_details(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    quantity_to_add = data['quantity']
    
    if user_id not in shopping_cart:
        shopping_cart[user_id] = {}
        
    cart = shopping_cart[user_id]
    
    if product_id not in cart:
        cart[product_id]['quantity'] += quantity_to_add
    else: 
        cart[product_id] = {
            'product_name': product['name'],
            'quantity': quantity_to_add,
            'total_price': product['price'] * quantity_to_add
        }
    return jsonify({"message": "Product added to cart"}), 201

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.json
    if 'quantity' not in data: 
        return jsonify({"error": "Quantity not specified"}), 400
    if user_id not in shopping_cart:
        return jsonify({"error": "Cart not found"}), 404
    
    cart = shopping_cart[user_id]
    
    if product_id not in cart:
        return jsonify({"error": "Product not found in cart"}), 404
    
    quantity_to_remove = data['quantity']
    if cart[product_id]['quantity'] <= quantity_to_remove:
        del cart[product_id]
    else:
        cart[product_id]['quantity'] -= quantity_to_remove
        cart[product_id]['total_price'] -= get_product_details(product_id)['price'] * quantity_to_remove
    
    return jsonify({"message": "Product removed from cart"}), 200

if __name__ == '__main__':
    app.run(debug=True)


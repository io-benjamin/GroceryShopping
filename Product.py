from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Apple", "price": 1.0, "quantity": 100},
    {"id": 2, "name": "Banana", "price": 0.5, "quantity": 50},
    {"id": 3, "name": "Orange", "price": 1.5, "quantity": 75},
    {"id": 4, "name": "Pineapple", "price": 3.0, "quantity": 25},
    {"id": 5, "name": "Mango", "price": 2.0, "quantity": 125},
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})

@app.route('/products/<int:products_id>', methods=['GET'])
def get_productID(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product: 
        return jsonify({"Product": product})
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = {
        "id": len(products) + 1,
        "name": data['name'],
        "price": data['price'],
        "quantity": data['quantity']
    }
    products.append(new_product)
        
    return jsonify({"message": "Product created", "Product": add_product}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)
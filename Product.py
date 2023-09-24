from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Apple", "price": 1.0, "quantity": 100},
    {"id": 2, "name": "Banana", "price": 0.5, "quantity": 50}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product: 
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    if 'name' not in data or 'price' not in data or 'quantity' not in data:
        new_product = {
            "id": len(products) + 1,
            "name": data['name'],
            "price": data['price'],
            "quantity": data['quantity']
        }
        products.append(new_product)
        return jsonify(new_product), 201
    return jsonify({"error": "Product not added"}), 400

if __name__ == '__main__':
    app.run(debug=True)
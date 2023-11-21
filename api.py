from flask import Flask, request, jsonify

app = Flask(__name__)   # creates a Flask web application

# In-memory data store (replace with a database in a real-world application)
users = []
products = []
orders = []

# User model
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Product model
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

# Order model
class Order:
    def __init__(self, id, user_id, product_id, status='Pending'):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.status = status

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'])
    users.append(new_user)
    return jsonify({'message': 'User registered successfully'})

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = next((user for user in users if user.username == data['username']), None)
    if user and user.password == data['password']:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Product listing endpoint
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Product details endpoint
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product.id == product_id), None)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price})
    else:
        return jsonify({'message': 'Product not found'}), 404

# Order creation endpoint
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    # Check if user and product exist
    user = next((user for user in users if user.id == user_id), None)
    product = next((product for product in products if product.id == product_id), None)

    if user and product:
        new_order = Order(id=len(orders) + 1, user_id=user_id, product_id=product_id)
        orders.append(new_order)
        return jsonify({'message': 'Order created successfully'})
    else:
        return jsonify({'message': 'User or product not found'}), 404

# Order retrieval endpoint
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify([{'id': order.id, 'user_id': order.user_id, 'product_id': order.product_id, 'status': order.status} for order in orders])

# Order status update endpoint
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    status = data.get('status')

    order = next((order for order in orders if order.id == order_id), None)
    if order:
        order.status = status
        return jsonify({'message': 'Order status updated successfully'})
    else:
        return jsonify({'message': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Create a Flask Instance 

# New MySQL DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_password@localhost/your_database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hey12345@localhost/database'
db = SQLAlchemy(app) # Initialize the database 


class User(db.Model):
    email = db.Column(db.String(60), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(60), db.ForeignKey('Email'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')

# Create the database tables
#db.create_all()

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(email=data['email'], username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.password == data['password']:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Product listing endpoint
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price} for product in products])

# Product details endpoint
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price})
    else:
        return jsonify({'message': 'Product not found'}), 404

# Order creation endpoint
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_email = data.get('user_email')  # Change to user_email
    product_id = data.get('product_id')

    # Check if user and product exist
    user = User.query.filter_by(email=user_email).first()
    product = Product.query.get(product_id)

    if user and product:
        new_order = Order(user_email=user_email, product_id=product_id)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'})
    else:
        return jsonify({'message': 'User or product not found'}), 404


# Order retrieval endpoint
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': order.id, 'user_email': order.user_email, 'product_id': order.product_id, 'status': order.status} for order in orders])

# Order status update endpoint
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    status = data.get('status')

    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'})
    else:
        return jsonify({'message': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

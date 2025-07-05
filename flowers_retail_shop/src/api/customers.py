from flask import Blueprint, request, jsonify
from ....models import Customer, db  # Import the Customer model and db

bp = Blueprint('customers', __name__, url_prefix='/customers')

# POST - Create a new customer
@bp.route('', methods=['POST'])
def create_customer():
    data = request.json
    if not all(key in data for key in ('first_name', 'last_name', 'email')):   # Check that all required are present in the JSON
        return jsonify({'error': 'Missing required fields'}), 400              # Errors if missing parameters

    customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(customer)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500   #  Error message with detials. 

    return jsonify(customer.serialize()), 201     # Data Created status

# GET - Retrieve all customers
@bp.route('', methods=['GET'])
def get_customers():
    customers = Customer.query.all()                                         # Fetch all customers from database
    return jsonify([c.serialize() for c in customers])                       # Searialize each customer and return as JSON list

# GET - Retrieve a single customer by ID
@bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)                               # Look up custome by primary Key
    if customer:
        return jsonify(customer.serialize())
    return jsonify({'error': 'Customer not found'}), 404                    # Error message customer not found

# PATCH - Partial update of a customer's details
@bp.route('/<int:customer_id>', methods=['PATCH'])
def update_customer(customer_id):
    data = request.json
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404                # Error message customer not found

    # Update only fields provided in the request
    if 'first_name' in data:
        customer.first_name = data['first_name']
    if 'last_name' in data:
        customer.last_name = data['last_name']
    if 'email' in data:
        customer.email = data['email']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500  #  Error message with detials.

    return jsonify(customer.serialize())                                      

# DELETE - Delete a customer by ID
@bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404                 # Error message customer not found

    db.session.delete(customer)                                              # Remove  from the database

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500  #  Error message with detials.

    return jsonify({'message': 'Customer deleted successfully'})             # Success message when deleted

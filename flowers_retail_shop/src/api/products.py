from flask import Blueprint, request, jsonify
from ....models import Product, db

bp = Blueprint('products', __name__, url_prefix='/products')

# POST - Create a new product
@bp.route('', methods=['POST'])
def create_products():
    data = request.get_json()

    # Ensure we're getting a list
    if not isinstance(data, list):
        return jsonify({'error': 'Expected a list of products'}), 400

    cur = db.session.connection().connection.cursor()
    created_ids = []

    try:
        for product_data in data:
            required_fields = ['owner_id', 'supplier_id', 'name', 'price']
            if not all(field in product_data for field in required_fields):
                return jsonify({'error': 'Missing required fields in one or more products'}), 400

            cur.execute(
                """
                INSERT INTO products (owner_id, supplier_id, name, price)
                VALUES (%s, %s, %s, %s)
                RETURNING product_id;
                """,
                (
                    product_data['owner_id'],
                    product_data['supplier_id'],
                    product_data['name'],
                    product_data['price']
                )
            )
            created_id = cur.fetchone()[0]
            created_ids.append(created_id)

        db.session.commit()
        return jsonify({'created_product_ids': created_ids}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500


# GET - Retrieve all products
@bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.serialize() for p in products])

# GET - Retrieve a single product by ID
@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.serialize())
    return jsonify({'error': 'Product not found'}), 404

# PATCH - Partial update for a product
@bp.route('/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.json
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if 'owner_id' in data:
        product.owner_id = data['owner_id']
    if 'supplier_id' in data:
        product.supplier_id = data['supplier_id']
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

    return jsonify(product.serialize())

# DELETE - Delete a product by ID
@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

    return jsonify({'message': 'Product deleted successfully'})

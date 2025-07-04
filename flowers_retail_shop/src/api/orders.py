from flask import Blueprint, request, jsonify
from .models import Order, db

bp = Blueprint('orders', __name__, url_prefix='/orders')

# POST - Create a new order
@bp.route('', methods=['POST'])
def create_order():
    data = request.json
    cur = db.session.connection().connection.cursor()
    cur.execute(
        """
        INSERT INTO orders (customer_id, order_date)
        VALUES (%s, %s) RETURNING order_id;
        """,
    (data['customer_id'], data['order_date'])
    )

    order_id = cur.fetchone()[0]
    db.session.commit()
    return jsonify({'order_id': order_id}), 201

# GET - Get all orders
@bp.route('', methods=['GET'])
def get_orders():
    cur = db.session.connection().connection.cursor()
    cur.execute("SELECT * FROM orders;")
    rows = cur.fetchall()
    return jsonify(rows)


# GET - Get single order by ID
@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    cur = db.session.connection().connection.cursor()
    cur.execute("SELECT * FROM orders WHERE order_id = %s;", (order_id,))
    row = cur.fetchone()
    if row:
        order = {
            'order_id': row[0],
            'customer_id': row[1],
            'order_date': str(row[2]),
        }
        return jsonify(order)
    else:
        return jsonify({'error': 'Order not found'}), 404


# PUT - Update an order by ID
@bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    cur = db.session.connection().connection.cursor()
    cur.execute(
        """
        UPDATE orders
        SET customer_id = %s, order_date = %s
        WHERE order_id = %s RETURNING order_id;
        """,
        (data['customer_id'], data['order_date'], order_id)
    )
    updated = cur.fetchone()
    if updated:
        db.session.commit()
        return jsonify({'message': f'Order {order_id} updated successfully.'})
    else:
        return jsonify({'error': 'Order not found'}), 404


# DELETE - Delete an order by ID
@bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    cur = db.session.connection().connection.cursor()
    cur.execute("DELETE FROM orders WHERE order_id = %s RETURNING order_id;", (order_id,))
    deleted = cur.fetchone()
    if deleted:
        db.session.commit()
        return jsonify({'message': f'Order {order_id} deleted successfully.'})
    else:
        return jsonify({'error': 'Order not found'}), 404

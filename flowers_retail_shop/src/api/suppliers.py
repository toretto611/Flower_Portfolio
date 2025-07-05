from flask import Blueprint, request, jsonify
from ....models import Supplier, db

bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

# POST - Create a new supplier
@bp.route('', methods=['POST'])
def create_supplier():
    data = request.json                                       # Get supplier data from request
    cur = db.session.connection().connection.cursor()
    cur.execute(
        "INSERT INTO suppliers (owner_id, name, contact_name, email) VALUES (%s, %s, %s, %s) RETURNING supplier_id;",
        (data['owner_id'], data['name'], data['contact_name'], data['email'])
    )
    supplier_id = cur.fetchone()[0]
    db.session.commit()
    return jsonify({'supplier_id': supplier_id}), 201       # Return new supplier ID with 201 Created status

# GET - Get all suppliers
@bp.route('', methods=['GET'])
def get_suppliers():
    cur = db.session.connection().connection.cursor()
    cur.execute("SELECT * FROM suppliers;")
    rows = cur.fetchall()
    return jsonify(rows)                                      # Return list of all suppliers

# GET - Get one supplier by ID
@bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    cur = db.session.connection().connection.cursor()
    cur.execute(
        "SELECT supplier_id, owner_id, name, contact_name, email FROM suppliers WHERE supplier_id = %s;",
        (supplier_id,)
    )
    row = cur.fetchone()
    if row:
        supplier = {
            'supplier_id': row[0],
            'owner_id': row[1],
            'name': row[2],
            'contact_name': row[3],
            'email': row[4]
        }
        return jsonify(supplier), 200
    else:
        return jsonify({'error': 'Supplier not found'}), 404


# PUT - Update a supplier by ID
@bp.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    data = request.json                                       # Get updated data from request
    cur = db.session.connection().connection.cursor()
    cur.execute(
        "UPDATE suppliers SET owner_id=%s, name=%s, contact_name=%s, email=%s WHERE supplier_id=%s RETURNING supplier_id;",
        (data['owner_id'], data['name'], data['contact_name'], data['email'], supplier_id)
    )
    updated = cur.fetchone()
    if updated:
        db.session.commit()
        return jsonify({'message': f'Supplier {supplier_id} updated successfully.'})
    else:
        return jsonify({'error': 'Supplier not found'}), 404

# DELETE- Delete a supplier by ID
@bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    cur = db.session.connection().connection.cursor()
    cur.execute("DELETE FROM suppliers WHERE supplier_id=%s RETURNING supplier_id;", (supplier_id,))
    deleted = cur.fetchone()
    if deleted:
        db.session.commit()
        return jsonify({'message': f'Supplier {supplier_id} deleted successfully.'})
    else:
        return jsonify({'error': 'Supplier not found'}), 404

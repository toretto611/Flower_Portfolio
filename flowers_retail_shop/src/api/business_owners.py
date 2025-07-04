from flask import Blueprint, request, jsonify
from .models import BusinessOwner, db  # Import your model and db instance

bp = Blueprint('business_owners', __name__, url_prefix='/business_owners')

#POST /owners - Add a new business owner
@bp.route('', methods=['POST'])
def create_owner():
    data = request.get_json()
    required_fields = ['user_id', 'first_name', 'last_name', 'email']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_owner = BusinessOwner(
            user_id=data['user_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
)
        db.session.add(new_owner)
        db.session.commit()
        return jsonify({'owner_id': new_owner.owner_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# GET /owners - Get all business owners
@bp.route('', methods=['GET'])
def get_owners():
    owners = BusinessOwner.query.all()
    return jsonify([owner.serialize() for owner in owners])

# GET - Get a specific business owner by ID
@bp.route('/<int:owner_id>', methods=['GET'])
def get_owner(owner_id):
    owner = BusinessOwner.query.get(owner_id)
    if owner:
        return jsonify(owner.serialize())
    else:
        return jsonify({'error': 'Business owner not found'}), 404

# PATCH - Update a business owner's information
@bp.route('/<int:owner_id>', methods=['PATCH'])
def update_owner(owner_id):
    data = request.json
    owner = BusinessOwner.query.get(owner_id)
    if not owner:
        return jsonify({'error': 'Business owner not found'}), 404

    try:
        if 'first_name' in data:
            owner.first_name = data['first_name']
        if 'last_name' in data:
            owner.last_name = data['last_name']
        if 'email' in data:
            owner.email = data['email']

        db.session.commit()
        return jsonify({'message': 'Business owner updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE - Delete a business owner by ID
@bp.route('/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    owner = BusinessOwner.query.get(owner_id)
    if not owner:
        return jsonify({'error': 'Business owner not found'}), 404

    try:
        db.session.delete(owner)
        db.session.commit()
        return jsonify({'message': 'Business owner deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    profile = db.relationship('UserProfile', backref='user', uselist=False)
    business_owner = db.relationship('BusinessOwner', backref='user', uselist=False)
    customer = db.relationship('Customer', backref='user', uselist=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column('profile_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    profile_picture = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'profile_picture': self.profile_picture
        }

class BusinessOwner(db.Model):
    __tablename__ = 'business_owners'
    owner_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def serialize(self):
        return {
            'owner_id': self.owner_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def serialize(self):
        return {
            'customer_id': self.customer_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('business_owners.owner_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            'supplier_id': self.supplier_id,
            'owner_id': self.owner_id,
            'name': self.name,
            'contact_name': self.contact_name,
            'email': self.email
        }

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('business_owners.owner_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def serialize(self):
        return {
            'product_id': self.product_id,
            'owner_id': self.owner_id,
            'supplier_id': self.supplier_id,
            'name': self.name,
            'price': float(self.price)
        }

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'order_date': self.order_date.isoformat() if self.order_date else None
        }

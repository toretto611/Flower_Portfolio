import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from ...models import db

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@pg:5432/my_blog',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)

    from .api import business_owners, customers, suppliers, products, orders
    app.register_blueprint(business_owners.bp)
    app.register_blueprint(customers.bp)
    app.register_blueprint(suppliers.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(orders.bp)

    @app.route('/')
    def home():
        return jsonify({"message": "Hi my_blog! Welcome to the API."})

    return app

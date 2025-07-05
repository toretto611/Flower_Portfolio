from flask import Flask
from models import db

# Initialize the Flask app
app = Flask(__name__)

# Configure the app to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flowers_user:password@db:5432/flowers_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to the Flower Shop API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

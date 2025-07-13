import sys
import os
import pytest

# Add the parent directory to the system path so it can find 'app.py'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Now import the app correctly

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')  # Make a GET request to the home route
    assert response.status_code == 200  # Check if the status code is 200
    assert b"Welcome to the Flower Shop API!" in response.data  # Check if the response contains this message

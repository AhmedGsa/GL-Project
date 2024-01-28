
from fastapi.testclient import TestClient
from main import app



client = TestClient(app)

def setup_function():
    # Register a new user
    register_json = {
        "email": "user@estin.dz",
        "password": "password",
        "nom": "user",
        "prenom": "new"
    }
    
    response = client.post("/auth/register-user", json=register_json)
    assert response.status_code == 200
    
def test_appointment():
    # Test case 1: Valid login credentials
    login_json = {
        "email": "user@estin.dz",
        "password": "password"
    }
    
    response = client.post("/auth/login", json=login_json)
    assert response.status_code == 200
    
    # Test case 2: InValid login credentials
    login_json = {
        "email": "InexistingUser#@estin.dz",
        "password": "password"
    }
    
    response = client.post("/auth/login", json=login_json)
    assert response.status_code == 404
    
def teardown_function():
    # Delete the user created during setup
    response = client.delete("/admin/users/user@estin.dz")
    assert response.status_code == 200
    
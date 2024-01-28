
from fastapi.testclient import TestClient
from main import app



client = TestClient(app)

def test_search():
    name = 'name'
    wilaya = 'Alger'
    categories = 'Family law'
    page = 1
    limit = 25
    
    # Test case : User search
    response = client.get('/search/search?name='+name+'&wilaya='+wilaya+'&categories='+categories+'&page='+str(page)+'&limit='+str(limit))
    assert response.status_code == 200
    
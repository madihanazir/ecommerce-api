# tests/test_response_format.py
import pytest

def test_response_format_categories():
    """Check categories endpoint returns correct format"""
    client = APIClient()
    response = client.get('/api/v1/categories/')
    
    assert response.status_code == 200
    data = response.json()
    
    # Check wrapper format
    assert 'success' in data
    assert 'data' in data
    assert 'error' in data  
    assert 'meta' in data
    
    assert data['success'] == True
    assert data['error'] is None
    assert isinstance(data['data'], list)
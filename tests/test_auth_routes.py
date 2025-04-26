def test_login_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Password' in response.data

def test_request_access_page_loads(client):
    response = client.get('/request_access')
    assert response.status_code == 200
    assert b'Request Account' in response.data
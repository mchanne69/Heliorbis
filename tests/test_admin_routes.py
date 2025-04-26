def test_admin_requires_login(client):
    response = client.get('/admin/', follow_redirects=True)
    assert b'Username' in response.data  # Redirects to login if not logged in
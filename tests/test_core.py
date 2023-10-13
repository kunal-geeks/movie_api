import json

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register_route(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_dashboard_route_for_admin(client, admin_token):
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert b'admin_dashboard' in response.data

def test_dashboard_route_for_user(client, user_token):
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert b'user_dashboard' in response.data

def test_edit_account_route_get(client, user_token):
    response = client.get('/edit-account', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert b'edit_account' in response.data

def test_edit_account_route_put(client,user_token):
   
    data = {'new_password': 'newpassword'}
    response = client.put('/edit-account', data=json.dumps(data), content_type='application/json',
                          headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert b'success' in response.data

def test_edit_account_route_put_without_new_password(client, user_token):
    response = client.put('/edit-account', data=json.dumps({}), content_type='application/json',
                          headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 400
    assert b'fail' in response.data

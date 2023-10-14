import json

def test_index_route(client):
    """
    This function is used to test the index route of the application.

    Parameters:
    - client: An object representing the client making the request.

    Returns:
    None
    """
    response = client.get('/')
    assert response.status_code == 200

def test_login_route(client):
    """
    Retrieves the login route from the client and asserts that the response status code is 200.

    Parameters:
    - client: The client object used to make the GET request.

    Returns:
    None
    """
    response = client.get('/login')
    assert response.status_code == 200

def test_register_route(client):
    """
    Test the registration route by sending a GET request to '/register' and asserting that the response status code is 200.

    Parameters:
    - client: The client object used to make the request.

    Return:
    - None
    """
    response = client.get('/register')
    assert response.status_code == 200

def test_dashboard_route_for_admin(client, admin_token):
    """
    Test the dashboard route for an admin user.

    Args:
        client (object): The client object used to make the HTTP request.
        admin_token (str): The admin token used for authentication.

    Returns:
        None
    """
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert b'admin_dashboard' in response.data

def test_dashboard_route_for_user(client, user_token):
    """
    Test the dashboard route for a user.

    Args:
        client (object): The client object for making requests.
        user_token (str): The user token for authentication.

    Returns:
        None
    """
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert b'user_dashboard' in response.data

def test_edit_account_route_get(client, user_token):
    """
    Sends a GET request to the '/edit-account' route with the specified user token.

    Parameters:
    - client: The client object used to send the request.
    - user_token: The token of the user.

    Returns:
    None
    """
    response = client.get('/edit-account', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert b'edit_account' in response.data

def test_edit_account_route_put(client,user_token):
    """
   Sends a PUT request to the '/edit-account' route with the provided client and user token.
   
   Args:
       client: The client to use for making the request.
       user_token: The user token to include in the request headers.
   
   Returns:
       None
   """
   
    data = {'new_password': 'newpassword'}
    response = client.put('/edit-account', data=json.dumps(data), content_type='application/json',
                          headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert b'success' in response.data

def test_edit_account_route_put_without_new_password(client, user_token):
    """
    Test the PUT request to edit the account without providing a new password.

    Parameters:
        client (object): The client object used to make the API request.
        user_token (string): The user token used for authentication.

    Returns:
        None
    """
    response = client.put('/edit-account', data=json.dumps({}), content_type='application/json',
                          headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 400
    assert b'fail' in response.data

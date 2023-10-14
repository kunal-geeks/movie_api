import json
import time
from urllib.parse import parse_qs, urlparse
import pytest
from app.models import BlacklistToken, User
from pytest_mock import mocker

TEST_USER_NAME = 'test'
TEST_USER_EMAIL = 'kunal.vbu@gmail.com'
TEST_PASSWORD = '123456'
OTHER_PASSWORD = '654321'
OTHER_EMAIL = 'kunal.ucet@gmail.com'

# helper functions to register a user
def register_user(client, name, email, password):
    """
    Registers a new user with the provided client.

    Args:
        client (object): The client object used to make the POST request.
        name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        object: The response object from the POST request.
    """
    return client.post(
        '/auth/register',
        data=json.dumps(dict(
            name=name,
            email=email,
            password=password
        )),
        content_type='application/json',
    )
    
def test_register_new_user(client):
    """
    Test the registration process for a new user.

    Parameters:
        client (object): The client object used to make HTTP requests.

    Returns:
        None
    """
    response = register_user(client, TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert 'auth_token' in data
    assert response.content_type == 'application/json'
    assert data['message'] == 'Successfully registered.'

def test_register_existing_user(client,db_session):
    """
    Test the register_user function when the user already exists in the database.

    Parameters:
    - client: The Flask test client.
    - db_session: The database session.

    Returns:
    - None
    """
    # Create a user first
    user = User(name=TEST_USER_NAME, email=TEST_USER_EMAIL, password=TEST_PASSWORD)
    db_session.add(user)
    db_session.commit()

    response = register_user(client, TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert data['status'] == 'fail'
    assert data['message'] == 'User already exists. Please Log in.'

def test_register_with_existing_email(client):
    """
    Test the registration process when using an existing email address.

    Args:
        client: The client object for making HTTP requests.

    Returns:
        None
    """
    # Create a user first
    response = register_user(client, TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD)
    assert response.status_code == 201
    # Create another user with the same email
    response = register_user(client, TEST_USER_NAME, TEST_USER_EMAIL, OTHER_PASSWORD)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert data['status'] == 'fail'
    assert data['message'] == 'Email address is already registered. Please use a different email.'


def test_login_success(client, mocker, db_session):
    """
    Test the successful login functionality.

    :param client: The test client for making requests.
    :type client: object
    :param mocker: The mocker object for mocking dependencies.
    :type mocker: object
    :param db_session: The database session object for testing.
    :type db_session: object

    :return: None
    :rtype: None
    """
    # Mocking the User object and db_session directly
    mocker.patch.object(User, 'encode_auth_token')
    mocker.patch.object(db_session, 'query', return_value=db_session.query(User))

    # Create a test user
    test_user = User(name=TEST_USER_NAME, email=TEST_USER_EMAIL, password=TEST_PASSWORD)
    db_session.add(test_user)
    db_session.commit()

    # Prepare the request data
    data = {
        'email': TEST_USER_EMAIL,
        'password': TEST_PASSWORD
    }

    # Mock the encode_auth_token method to return a sample token
    User.encode_auth_token.return_value = 'sample_access_token'

    # Send a POST request to the login endpoint
    response = client.post('auth/login', json=data, content_type='application/json')

    # Verify the response
    assert response.status_code == 200
    assert 'auth_token' in response.json
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Successfully logged in.'
    assert response.content_type == 'application/json'
    assert response.json['auth_token'] == 'sample_access_token'

def test_non_registered_user_login(client, mocker, db_session):
    """
    Test the login functionality for a non-registered user.

    Parameters:
    - client: The client object used to make HTTP requests.
    - mocker: The mocker object used for mocking.
    - db_session: The database session object.

    Returns:
    None
    """
    # Mocking the User object and db_session directly
    mocker.patch.object(User, 'encode_auth_token')
    mocker.patch.object(db_session, 'query', return_value=db_session.query(User))

    # Prepare the request data with a non-existing email
    data = {
        'email': OTHER_EMAIL,
        'password': OTHER_PASSWORD
    }

    # Mock the encode_auth_token method to return None
    User.encode_auth_token.return_value = None

    # Send a POST request to the login endpoint
    response = client.post('auth/login', json=data, content_type='application/json')

    # Verify the response
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'User does not exist.'

def test_login_with_invalid_password(client, mocker, db_session):
    """
    Tests the login functionality with an invalid password.

    Parameters:
    - client: The test client for making HTTP requests.
    - mocker: The mocker object for mocking dependencies.
    - db_session: The database session object.

    Returns:
    None
    """
    # Mocking the User object and db_session directly
    mocker.patch.object(User, 'encode_auth_token')
    mocker.patch.object(db_session, 'query', return_value=db_session.query(User))

    # Create a test user
    test_user = User(name=TEST_USER_NAME, email=TEST_USER_EMAIL, password=TEST_PASSWORD)
    db_session.add(test_user)
    db_session.commit()

    # Prepare the request data
    data = {
        'email': TEST_USER_EMAIL,
        'password': OTHER_PASSWORD
    }

    # Send a POST request to the login endpoint
    response = client.post('auth/login', json=data, content_type='application/json')

    # Verify the response
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'Incorrect password.'
    
    
def test_status_with_valid_token(client, db_session):
    """
    Test the status endpoint with a valid authentication token.

    Args:
        client: The test client object.
        db_session: The database session object.

    Returns:
        None
    """
    # Create a test user and encode a valid auth token
    test_user = User(name=TEST_USER_NAME, email=TEST_USER_EMAIL, password=TEST_PASSWORD, admin=True)
    db_session.add(test_user)
    db_session.commit()
    auth_token = test_user.encode_auth_token(test_user.id)

    # Set the Authorization header with the valid token
    headers = {'Authorization': f'Bearer {auth_token}'}

    # Send a GET request to the /status endpoint with the valid token
    response = client.get('auth/status', headers=headers, content_type='application/json')

    # Verify the response
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['user_id'] == test_user.id
    assert data['email'] == 'kunal.vbu@gmail.com'
    assert data['admin'] is True
    assert data['registered_on'] == test_user.registered_on.strftime('%a, %d %b %Y %H:%M:%S GMT')
    assert response.json['status'] == 'success'
    assert response.content_type == 'application/json'
    

def test_status_with_invalid_token(client):
    """
    Test the status endpoint with an invalid token.

    Parameters:
        client (object): The client object used to send requests.

    Returns:
        None
    """
    # Set an invalid Authorization header
    headers = {'Authorization': 'Bearer invalid_token'}

    # Send a GET request to the /status endpoint with the invalid token
    response = client.get('auth/status', headers=headers)

    # Verify the response
    assert response.status_code == 401
    assert response.get_json()['status'] == 'fail'
    assert response.get_json()['message'] == 'Invalid token. Please log in again.'

def test_status_without_token(client):
    """
    Sends a GET request to the /status endpoint without the Authorization header.

    Parameters:
        client (object): The client object used to make the request.

    Returns:
        None
    """
    # Send a GET request to the /status endpoint without the Authorization header
    response = client.get('auth/status')

    # Verify the response
    assert response.status_code == 401
    assert response.get_json()['status'] == 'fail'
    assert response.get_json()['message'] == 'Provide a valid auth token.'

def test_logout_with_missing_token(client):
    """
    Test the logout functionality when the authentication token is missing.
    
    Args:
        client: The test client for making HTTP requests.
    
    Returns:
        None
        
    Raises:
        AssertionError: If any of the assertions fail.
    """
    response = client.post('/auth/logout', follow_redirects=True)
    assert response.status_code == 401  # Assume the logout endpoint returns 200 OK on success
    
    # Check if the response is a redirect to the login page
    assert response.status_code == 401
    assert '/login' in response.location  # Check if it redirects to the login page
    
    # Parse the query parameters of the redirected URL
    redirected_url = urlparse(response.location)
    query_params = parse_qs(redirected_url.query)
    
    # Check if the 'error' query parameter contains the correct message
    assert 'error' in query_params
    assert query_params['error'][0] == 'Token is missing'

def test_logout_with_invalid_token(client, mocker):
    """
    Test the logout functionality with an invalid token.
    
    Args:
        client: The client object used to make HTTP requests.
        mocker: The mocker object used for patching the 'blacklist_token' function.
    
    Returns:
        None
    """
    mocker.patch('app.routes.auth.blacklist_token', return_value=False)
    auth_header = {'Authorization': 'Bearer invalid_auth_token'}
    response = client.post('/auth/logout', headers=auth_header, follow_redirects=True)
    assert response.status_code == 401  # Assume the logout endpoint returns 200 OK on success
    
    # Check if the response is a redirect to the login page
    assert response.status_code == 401
    assert '/login' in response.location  # Check if it redirects to the login page
    
    # Parse the query parameters of the redirected URL
    redirected_url = urlparse(response.location)
    query_params = parse_qs(redirected_url.query)
    # Check if the 'error' query parameter contains the correct message
    assert 'error' in query_params
    assert query_params['error'][0] == 'Invalid token'


@pytest.mark.parametrize("name, email, password, expected_status, expected_message", [
    (TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD, 401, 'Signature expired. Please log in again.'),
])
def test_invalid_logout(client, name, email, password, expected_status, expected_message):
    """
    Test for invalid logout with expired token.

    Args:
        client: The test client.
        name: The name of the user.
        email: The email of the user.
        password: The password of the user.
        expected_status: The expected HTTP status code.
        expected_message: The expected error message.

    Returns:
        None
    """
    # user registration
    resp_register = register_user(client, name, email, password)
    assert resp_register.status_code == 201

    # user login
    resp_login = client.post(
        '/auth/login',
        data=json.dumps({'email': email, 'password': password}),
        content_type='application/json'
    )
    assert resp_login.status_code == 200

    # Wait for token to expire
    time.sleep(6)  # Adjust sleep duration based on your token expiration time

    # Attempt to logout with expired token
    auth_token = resp_login.get_json().get('auth_token', '')
    response = client.post(
        '/auth/logout',
        headers={'Authorization': f'Bearer {auth_token}'},
        follow_redirects=False  # Disable automatic redirection
    )

    # Check if the response is a redirection to the login page
    assert response.status_code == expected_status
    assert '/login' in response.location

    response = User.decode_auth_token(auth_token)
    assert response == expected_message
 
# Test user status
def test_valid_blacklisted_token_logout(client, db_session):
    """
    Function to test the logout functionality when a valid token is blacklisted.
    
    Parameters:
    - client: Flask test client object.
    - db_session: Database session object.
    
    Returns:
    None
    """
    # User registration
    resp_register = register_user(client, name=TEST_USER_NAME, email=TEST_USER_EMAIL, password=TEST_PASSWORD)
    assert resp_register.status_code == 201

    # User login
    resp_login = client.post(
        '/auth/login',
        data=json.dumps({
            'email': TEST_USER_EMAIL,
            'password': TEST_PASSWORD
        }),
        content_type='application/json'
    )
    assert resp_login.status_code == 200

    # Blacklist a valid token
    auth_token = resp_login.get_json()['auth_token']
    assert auth_token is not None  # Ensure the auth_token is present in the response

    blacklist_token = BlacklistToken(token=auth_token)
    db_session.add(blacklist_token)
    db_session.commit()

    # Blacklisted valid token logout
    resp_logout = client.post(
        '/auth/logout',
        headers={'Authorization': f'Bearer {auth_token}'},
        follow_redirects=False  # Disable automatic redirection
    )
    
    # Check if the response is a redirection to the login page
    assert resp_logout.status_code == 401
    assert '/login' in resp_logout.location
    
    response = User.decode_auth_token(auth_token)
    assert response == 'Token blacklisted. Please log in again.'
    
def test_valid_blacklisted_token_user(client, db_session):
    """
    Test the functionality of blacklisting a valid token for a user.

    Parameters:
    - client: The client object for making HTTP requests.
    - db_session: The database session object.

    Returns:
    None
    """
    # User registration
    resp_register = register_user(client, TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD)
    assert resp_register.status_code == 201
    auth_token = resp_register.get_json()['auth_token']

    # Blacklist a valid token
    blacklist_token = BlacklistToken(token=auth_token)
    db_session.add(blacklist_token)
    db_session.commit()

    # Attempt to access user status with the blacklisted token
    resp_status = client.get(
        '/auth/status',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    data_status = resp_status.get_json()
    assert resp_status.status_code == 401
    assert data_status['status'] == 'fail'
    assert data_status['message'] == 'Token blacklisted. Please log in again.'

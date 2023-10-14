def test_get_movies_user(client, user_token):
    """
    Function to test the `get_movies` endpoint with a user's authorization token.
    
    Parameters:
        client (object): The client object used to send HTTP requests.
        user_token (str): The authorization token of the user.
    
    Returns:
        None
    """
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/get_movies', headers=headers)
    assert response.status_code == 200

def test_get_genres_user(client, user_token):
    """
    Test the 'get_genres_user' function.

    Args:
        client: The client object for making HTTP requests.
        user_token: The token of the user making the request.

    Returns:
        None
    """
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/get_genres', headers=headers)
    assert response.status_code == 200

def test_add_movie_user(client, user_token):
    """
    Test the functionality of adding a movie by a user.

    Args:
        client (object): The client object representing the API client.
        user_token (str): The authorization token of the user.

    Returns:
        None
    """
    headers = {'Authorization': f'Bearer {user_token}'}
    movie_data = {
        'name': 'New Movie',
        'director': 'Director Name',
        'popularity': 7.8,
        'imdb_score': 8.0,
        'genre': ['Action', 'Adventure']
    }
    response = client.post('/api/movies', json=movie_data, headers=headers)
    assert response.status_code == 403  # Assuming the endpoint returns 403 for unauthorized access

def test_manage_movie_user(client, user_token):
    """
    Updates a movie's information using the provided client and user token.

    Args:
        client (object): The client object used to make HTTP requests.
        user_token (str): The user token used for authorization.

    Returns:
        None
    """
    headers = {'Authorization': f'Bearer {user_token}'}
    movie_id = 1  # Assuming a valid movie ID for testing
    updated_data = {
        'name': 'Updated Movie Name',
        'director': 'Updated Director',
        'popularity': 8.0,
        'imdb_score': 9.0,
        'genre': ['Comedy']
    }
    response = client.put(f'/api/movies/{movie_id}', json=updated_data, headers=headers)
    assert response.status_code == 403  # Assuming the endpoint returns 403 for unauthorized access

def test_get_movie_logs_user(client, user_token):
    """
    Get the movie logs for a specific user.

    Args:
        client: The client object used to make the API request.
        user_token: The user token used for authentication.

    Returns:
        None
    """
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/movie_logs', headers=headers)
    assert response.status_code == 403  # Assuming the endpoint returns 403 for unauthorized access

def test_add_movie_admin(client, admin_token):
    """
    Function to test the addition of a movie by an admin user.

    Parameters:
    - client: The client object for making HTTP requests.
    - admin_token: The authentication token for the admin user.

    Returns:
    - None

    Raises:
    - AssertionError: If the response status code is not equal to 201.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    movie_data = {
        'name': 'New Movie',
        'director': 'Director Name',
        'popularity': 7.8,
        'imdb_score': 8.0,
        'genre': ['Action', 'Adventure']
    }
    response = client.post('/api/movies', json=movie_data, headers=headers)
    assert response.status_code == 201

def test_manage_movie_admin(client, admin_token):
    """
    Tests the functionality of the manage_movie_admin function.

    Parameters:
    - client: an instance of the client class used for making HTTP requests
    - admin_token: a string representing the admin token used for authentication

    Returns:
    - None

    Raises:
    - AssertionError: if the response status code is not equal to 200
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    movie_id = 1  # Assuming a valid movie ID for testing
    updated_data = {
        'name': 'Updated Movie Name',
        'director': 'Updated Director',
        'popularity': 8.0,
        'imdb_score': 9.0,
        'genre': ['Comedy']
    }
    response = client.put(f'/api/movies/{movie_id}', json=updated_data, headers=headers)
    assert response.status_code == 200

def test_get_movie_logs_admin(client, admin_token):
    """
    Retrieves movie logs using the admin token.

    :param client: The client object used to make the API request.
    :type client: object
    :param admin_token: The admin token used for authentication.
    :type admin_token: str
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/movie_logs', headers=headers)
    assert response.status_code == 200

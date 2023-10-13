def test_get_movies_user(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/get_movies', headers=headers)
    assert response.status_code == 200

def test_get_genres_user(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/get_genres', headers=headers)
    assert response.status_code == 200

def test_add_movie_user(client, user_token):
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
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/movie_logs', headers=headers)
    assert response.status_code == 403  # Assuming the endpoint returns 403 for unauthorized access

def test_add_movie_admin(client, admin_token):
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
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/movie_logs', headers=headers)
    assert response.status_code == 200

import os
import sys

# Add the application root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

def test_app_is_testing():
    app = create_app('testing')
    db_path = os.path.join(app.config['BASE_DIR'], 'instance', 'test.db')
    assert app.testing is True
    assert app.config['DEBUG'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + db_path
    assert app.config['BCRYPT_LOG_ROUNDS'] == 4
    assert 'SECRET_KEY' in app.config  # Assert that 'SECRET_KEY' is in the app's configuration
    assert app.config['SECRET_KEY'] is not None  # Assert that SECRET_KEY is defined and not None
    assert isinstance(app.config['SECRET_KEY'], str)  # Assert that SECRET_KEY is a string
    assert len(app.config['SECRET_KEY']) >= 16  # Assert that SECRET_KEY is at least 16 characters long
    assert app.config['WTF_CSRF_ENABLED'] is False 

def test_app_is_development():
    app = create_app(test_config=None)
    db_path = os.path.join(app.config['BASE_DIR'], 'instance', 'movies.db')
    assert app.testing is False
    assert app.config['DEBUG'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + db_path
    assert app.config['BCRYPT_LOG_ROUNDS'] == 14
    assert 'SECRET_KEY' in app.config  # Assert that 'SECRET_KEY' is in the app's configuration
    assert app.config['SECRET_KEY'] is not None  # Assert that SECRET_KEY is defined and not None
    assert isinstance(app.config['SECRET_KEY'], str)  # Assert that SECRET_KEY is a string
    assert len(app.config['SECRET_KEY']) >= 16  # Assert that SECRET_KEY is at least 16 characters long

def test_app_is_production():
    app = create_app(test_config='production')
    db_path = os.path.join(app.config['BASE_DIR'], 'instance', 'movies.db')
    assert app.testing is False
    assert app.config['DEBUG'] is False
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + db_path
    assert app.config['BCRYPT_LOG_ROUNDS'] == 14
    assert 'SECRET_KEY' in app.config  # Assert that 'SECRET_KEY' is in the app's configuration
    assert app.config['SECRET_KEY'] is not None  # Assert that SECRET_KEY is defined and not None
    assert isinstance(app.config['SECRET_KEY'], str)  # Assert that SECRET_KEY is a string
    assert len(app.config['SECRET_KEY']) >= 16  # Assert that SECRET_KEY is at least 16 characters long


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

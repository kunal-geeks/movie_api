import os
import sys

# Add the application root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

def test_app_is_testing():
    """
    Test the create_app function with the 'testing' configuration.

    This function creates an instance of the Flask application using the 'testing' configuration.
    It then asserts that the application is in testing mode and that the debug mode is enabled.
    It also asserts that the SQLAlchemy database URI is set to a SQLite database located in the 'instance' directory.
    The function further asserts that the bcrypt log rounds are set to 4.
    It checks if the 'SECRET_KEY' configuration variable is present in the application's configuration dictionary.
    It also verifies that the 'SECRET_KEY' variable is defined and not None, and that it is of type string.
    Additionally, the function asserts that the length of the 'SECRET_KEY' is at least 16 characters.
    Finally, it asserts that the 'WTF_CSRF_ENABLED' configuration variable is set to False.

    Parameters:
    None

    Returns:
    None
    """
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
    """
    Test if the application is in development mode.

    This function creates an application instance using the `create_app` function with the `test_config` parameter set to `None`. It then checks various configuration values of the application instance to ensure that it is in development mode.

    Parameters:
    None

    Returns:
    None
    """
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
    """
    Check if the application is running in a production environment.

    This function creates an instance of the application using the 'create_app' function with the 'test_config' parameter set to 'production'. It then checks various configuration values of the application to ensure that it is configured correctly for a production environment.

    Parameters:
        None

    Returns:
        None
    """
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
    """
    This function sends a GET request to the '/hello' endpoint of the client and asserts that the response data is equal to the byte string 'Hello, World!'.

    :param client: The client used to make the GET request.
    :type client: <type of client>
    """
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

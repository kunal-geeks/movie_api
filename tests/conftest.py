import os
import sys
import pytest

# Add the application root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.database import init_db, drop_db, db
from app.models import User

TEST_USER_NAME = 'test'
TEST_EMAIL = 'kunal.vbu@gmail.com'
TEST_PASSWORD = '123456'


@pytest.fixture(scope="function")
def app():
    app = create_app(test_config='testing')
    with app.app_context():
        init_db()  # Initialize the database
        from db_utils import load_data_from_json
        load_data_from_json('imdb.json', app)  # Load data for testing
        yield app
        with app.app_context():
            drop_db()   # Drop the tables

@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        # Create a new database session for each test
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        session = db._make_scoped_session(options=options)
        yield session
        transaction.rollback()
        connection.close()
        session.remove()

@pytest.fixture
def runner(app):
    # Provide a CLI runner for testing Flask CLI commands
    return app.test_cli_runner()

@pytest.fixture
def g():
    # Provide a clean g object for each test
    g = app.app_context().globals
    yield g
    g.clear()

@pytest.fixture
def user_token(client):
    # Register user
    user_data = {
        'name': TEST_USER_NAME,
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    }
    client.post('/auth/register', json=user_data)
    
    # Login user and return token
    login_data = {
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    return response.json['auth_token']

@pytest.fixture
def admin_token(client, db_session):
    # Create admin user if it doesn't exist
    admin = db_session.get(User,TEST_EMAIL)
    if not admin:
        admin = User(name=TEST_USER_NAME, email=TEST_EMAIL, password=TEST_PASSWORD, admin=True)
        db_session.add(admin)
        db_session.commit()

    # Login admin and return token
    login_data = {
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    return response.json['auth_token']

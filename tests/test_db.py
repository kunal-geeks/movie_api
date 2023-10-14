from sqlalchemy import inspect
from app import create_app
from app.database import get_db
def test_init_db_command(runner, monkeypatch):
    """
    Test the initialization of the database command.

    Parameters:
    - runner: The test runner object.
    - monkeypatch: The monkeypatch object.

    Returns:
    None
    """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    app = create_app()

    # Push an application context before calling the fake_init_db function
    with app.app_context():
        monkeypatch.setattr('app.database.init_db', fake_init_db)
        result = runner.invoke(args=['init-db'])
        assert 'Initialized the database.' in result.output
        assert Recorder.called

    # Optionally, you can check if the necessary tables were created
    with app.app_context():
        db = get_db()
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        assert 'users' in tables  # Replace 'users' with the name of your user table


def test_client(client):
    """
    Test the client by sending a GET request to the root route and checking if the response status code is 200.

    :param client: The client to test.
    :type client: object

    :return: None
    """
    response = client.get('/')
    assert response.status_code == 200  # Check if the root route returns a okay status code

def test_db_session(db_session):
    """
    Verifies that the given database session is not None.
    
    Args:
        db_session: The database session object to be verified.
    
    Returns:
        None
    """
    assert db_session is not None

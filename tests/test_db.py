from sqlalchemy import inspect
from app import create_app
from app.database import get_db
def test_init_db_command(runner, monkeypatch):
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
    response = client.get('/')
    assert response.status_code == 200  # Check if the root route returns a okay status code

def test_db_session(db_session):
    assert db_session is not None

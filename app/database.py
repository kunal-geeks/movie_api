import click
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()

def init_db():
    """
    Initializes the database by creating all the necessary tables.

    This function should be called before starting to use the database.
    It creates all the tables defined in the database schema.

    Parameters:
        None

    Returns:
        None
    """
    with current_app.app_context():
        db.create_all()

def drop_db():
    """
    Drops the entire database.

    This function is used to drop all the tables and other objects in the database. It should be used with caution as it permanently deletes all the data in the database.

    Parameters:
        None

    Returns:
        None
    """
    with current_app.app_context():
        db.drop_all()

def get_db():
    """
    Retrieves the database session object.

    :return: The database session object.
    """
    if not hasattr(g, '_database'):
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        g._database = scoped_session(sessionmaker(bind=engine))
    return g._database

def close_db(e=None):
    """
    Closes the database connection.

    :param e: An optional exception object. Default is None.
    :return: None
    """
    database = getattr(g, '_database', None)
    if database is not None:
        database.remove()

@click.command('init-db')
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo('Initialized the database.')

@click.command('drop-db')
def drop_db_command():
    """Drop the database."""
    drop_db()
    click.echo('Dropped the database.')

# Register the commands as Flask CLI commands
def init_app(app):
    """
    Initializes the application by setting up the necessary teardown and CLI commands.

    Args:
        app: The Flask application object.

    Returns:
        None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)

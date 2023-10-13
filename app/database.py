import click
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()

def init_db():
    with current_app.app_context():
        db.create_all()

def drop_db():
    with current_app.app_context():
        db.drop_all()

def get_db():
    if not hasattr(g, '_database'):
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        g._database = scoped_session(sessionmaker(bind=engine))
    return g._database

def close_db(e=None):
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
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)

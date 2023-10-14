import os
from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.database import db

# Initialize Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Args:
        test_config (str, optional): The configuration type for testing purposes. Defaults to None.

    Returns:
        Flask: The Flask application instance.
    """    
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the appropriate configuration for the environment
    if test_config is None:
        app.config.from_object(DevelopmentConfig)  # Use your desired default config class
    elif test_config == 'testing':
        app.config.from_object(TestingConfig) 
    else: 
        app.config.from_object(ProductionConfig)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Flask extensions with the app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Import and register your blueprints, routes, and other application components here
        from app.routes import core, auth, movies

        # Register the blueprints
        app.register_blueprint(core.core_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(movies.api_bp)
    
        from app.database import init_app, init_db
        
        # Register the init_db_command as a Flask CLI command
        init_app(app)
        # Initialize the database
        init_db() 
    
        # For testing purposes
        @app.route('/hello')
        def hello():
            return 'Hello, World!'

        
        @app.route('/docs/<path:filename>')
        def serve_docs(filename):
            docs_dir = os.path.join(os.getcwd(), 'docs')  # Ensure 'docs' is in the correct directory
            return send_from_directory(docs_dir + '/build', filename)

    return app

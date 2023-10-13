import os
import secrets

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))  # Generate a secure random string
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))  # Generate a secure random string
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'strict'
    BCRYPT_LOG_ROUNDS = 14
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'instance', 'movies.db')
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'instance', 'movies.db')  
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'instance', 'test.db')
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    JWT_ACCESS_TOKEN_EXPIRES = 5

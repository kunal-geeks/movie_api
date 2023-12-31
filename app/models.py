import datetime
import json
import bcrypt
import jwt
from flask import current_app
from app.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Updated data type
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, admin=False):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)  # hash the password
        self.registered_on = datetime.datetime.utcnow()
        self.admin = admin
    
    def _hash_password(self, password):
        """
        Hashes a given password using bcrypt.

        Parameters:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
        
    def check_password(self, password):
        """
        Checks if the provided password matches the stored password.

        Parameters:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')) 
    def encode_auth_token(self, expires_in):
        """
        Generates an authentication token for the user.

        Args:
            expires_in (int): The number of seconds for which the token will be valid.

        Returns:
            str: The encoded authentication token.

        Raises:
            Exception: If an error occurs while encoding the token.
        """
        try:
            now = datetime.datetime.utcnow()
            payload = {
                'exp': now + datetime.timedelta(seconds=expires_in),
                'iat': now,
                'sub': self.id
            }
            return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        

class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
    
    @staticmethod
    def check_blacklist(auth_token):
        from app.database import get_db, close_db
        db_session = get_db()
        # check whether auth token has been blacklisted
        res = db_session.query(BlacklistToken).filter_by(token=str(auth_token)).first()
        close_db()
        if res:
            return True  
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(255), nullable=False)  # Store genres as JSON strings
    popularity = db.Column(db.Float, nullable=False)
    imdb_score = db.Column(db.Float, nullable=False)

    def set_genre(self, genres):
        """
        Set the genre of the object.

        Args:
            genres (list): A list of genres to set.

        Returns:
            None
        """
        self.genre = json.dumps(genres)  # Convert list to JSON string for storage
    
    def get_genre(self):
        """
        Parses a JSON string representing a genre list and returns the parsed list.

        Returns:
            list: The parsed genre list.
        """
        return json.loads(self.genre) if self.genre else []  # Parse JSON string back to list

    def serialize(self):
        """
        Serializes the object into a dictionary representation.

        Returns:
            dict: A dictionary containing the serialized object.
                The dictionary has the following keys:
                - 'id' (int): The ID of the object.
                - 'name' (str): The name of the object.
                - 'director' (str): The director of the object.
                - 'genre' (list): The genre(s) of the object, retrieved as a list.
                - 'popularity' (float): The popularity score of the object.
                - 'imdb_score' (float): The IMDb score of the object.
                - ... (other attributes as needed)
        """
        return {
            'id': self.id,
            'name': self.name,
            'director': self.director,
            'genre': self.get_genre(),  # Retrieve genres as a list
            'popularity': self.popularity,
            'imdb_score': self.imdb_score,
            # Add other attributes as needed
        }
        
class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    movie = db.relationship('Movie', backref='genres')

    def serialize(self):
        """
        Serializes the object into a dictionary.

        Returns:
            dict: A dictionary representation of the object with the following keys:
                  - 'id' (int): The ID of the object.
                  - 'name' (str): The name of the object.
                  - 'movie_id' (int): The ID of the movie associated with the object.
                  - 'movie' (dict or None): A dictionary representation of the associated movie
                                            if it exists, otherwise None.
        """
        return {
            'id': self.id,
            'name': self.name,
            'movie_id': self.movie_id,
            'movie': self.movie.serialize() if self.movie else None,
            # Add other attributes as needed
        }

class MoviesLog(db.Model):
    __tablename__ = 'movies_logs'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    movie_name = db.Column(db.String(100))
    action = db.Column(db.String(10))  # ADDED, UPDATED, DELETED
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, movie_id, movie_name, action):
        """
        Initializes a new instance of the class.

        Parameters:
            movie_id (int): The ID of the movie.
            movie_name (str): The name of the movie.
            action (str): The action to be performed.

        Returns:
            None
        """
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.action = action




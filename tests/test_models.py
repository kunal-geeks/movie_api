from app.models import BlacklistToken, User, Movie, Genre, MoviesLog

def test_user_model(app, db_session):
    with app.app_context():
        user = User(name='Test User', email='test@example.com', password='password')
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert db_session.get(User,user.id) == user
        assert user.check_password('password') is True

def test_movie_model(app, db_session):
    with app.app_context():
        # Create a movie with genres provided as a list
        movie = Movie(name='Test Movie', director='Director', popularity=7.5, imdb_score=8.0)
        movie.set_genre(['Action', 'Adventure'])  # Convert list to JSON string
        db_session.add(movie)
        db_session.commit()

        assert movie.id is not None
        assert db_session.get(Movie,movie.id) == movie
        assert movie.serialize() == {
            'id': movie.id,
            'name': 'Test Movie',
            'director': 'Director',
            'genre': ['Action', 'Adventure'],
            'popularity': 7.5,
            'imdb_score': 8.0
        }

def test_genre_model(app, db_session):
    with app.app_context():
        movie = Movie(name='Test Movie', director='Director', popularity=7.5, imdb_score=8.0)
        movie.set_genre(['Action'])
        genre = Genre(name='Action', movie=movie)
        db_session.add_all([movie, genre])
        db_session.commit()

        assert genre.id is not None
        assert db_session.get(Genre,genre.id) == genre
        assert genre.serialize() == {
            'id': genre.id,
            'name': 'Action',
            'movie_id': movie.id,
            'movie': movie.serialize()
        }

def test_movies_log_model(app, db_session):
    with app.app_context():
        log = MoviesLog(movie_id=1, movie_name='Test Movie', action='ADDED')
        db_session.add(log)
        db_session.commit()

        assert log.id is not None
        assert db_session.get(MoviesLog,log.id) == log

def test_blacklist_token_model(app, db_session):
    with app.app_context():
        token = 'test_token'
        blacklist_token = BlacklistToken(token=token)
        db_session.add(blacklist_token)
        db_session.commit()

        assert blacklist_token.id is not None
        assert db_session.get(BlacklistToken,blacklist_token.id) == blacklist_token

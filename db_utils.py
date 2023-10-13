import json
from app.database import get_db, close_db
from app.models import Movie, Genre, User, BlacklistToken

def empty_database():
    db_session = get_db()
    db_session.query(Movie).delete()
    db_session.query(Genre).delete()
    db_session.query(User).delete()
    db_session.query(BlacklistToken).delete()
    db_session.commit()
    db_session.close()

def load_data_from_json(filename, app):
    with app.app_context():
        db_session = get_db()
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for movie_data in data:
                    movie = Movie(
                        name=movie_data['name'],
                        director=movie_data['director'],
                        popularity=movie_data['99popularity'],
                        imdb_score=movie_data['imdb_score'],
                    )
                    movie.set_genre(movie_data['genre'])  # Set genres using the set_genre method
                    db_session.add(movie)
                    db_session.flush()  # This ensures that movie.id is populated before creating genres
                    for genre_name in movie_data['genre']:
                        genre = Genre(name=genre_name, movie_id=movie.id)
                        db_session.add(genre)
                db_session.commit()
            print("Data has been successfully populated into the database.")
        except FileNotFoundError as e:
            print(f"Error: {e}. Please provide the correct path to 'imdb.json'.")
        except Exception as e:
            db_session.rollback()
            print(f"An error occurred while populating the database: {e}")
        finally:
            close_db()

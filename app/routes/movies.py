from flask import Blueprint, g, jsonify, request
from app.models import Movie, Genre, MoviesLog
from app.database import get_db
from app.decorators import token_required
from sqlalchemy import or_

db_session = get_db()

api_bp = Blueprint('api', __name__, url_prefix='/api')

# both and user can access 
@api_bp.route('/get_movies', methods=['GET'])
@token_required
def get_movies():
    page = request.args.get('page', 1, type=int)
    genre_filter = request.args.get('genre', '', type=str)
    sort_by = request.args.get('sort', 'imdb_score', type=str)
    order = request.args.get('order', 'asc', type=str)
    search_query = request.args.get('search', '', type=str)

    movies_query = Movie.query

    if genre_filter:
        genre_movies = db_session.query(Genre.movie_id).filter_by(name=genre_filter).all()
        movie_ids = [movie_id for movie_id, in genre_movies]
        movies_query = movies_query.filter(Movie.id.in_(movie_ids))

    if sort_by == 'imdb_score':
        if order == 'asc':
            movies_query = movies_query.order_by(Movie.imdb_score.asc())
        else:
            movies_query = movies_query.order_by(Movie.imdb_score.desc())
    elif sort_by == 'popularity':
        if order == 'asc':
            movies_query = movies_query.order_by(Movie.popularity.asc())
        else:
            movies_query = movies_query.order_by(Movie.popularity.desc())

    if search_query:
        # Check if search query is a numeric value (ID search)
        if search_query.isdigit():
            movies_query = movies_query.filter(or_(Movie.id == int(search_query)))
        else:
            movies_query = movies_query.filter(or_(Movie.name.ilike(f'%{search_query}%'),
                                                   Movie.director.ilike(f'%{search_query}%')))


    per_page = 10
    movies = movies_query.paginate(page=page, per_page=per_page, error_out=False)

    movies_list = []
    for movie in movies.items:
        movies_list.append(movie.serialize())

    return jsonify({
        'movies': movies_list,
        'total_pages': movies.pages
    }), 200

# both admin and user can access
@api_bp.route('/get_genres', methods=['GET'])
@token_required
def get_genres():
    genres = db_session.query(Genre.name.distinct()).all()
    unique_genres = [genre[0] for genre in genres]
    return jsonify({'genres': unique_genres}), 200

# only admin can access
@api_bp.route('/movies', methods=['POST'])
@token_required
def add_movie():
    if not g.user.admin:
        return jsonify(message='Admin privilege required'), 403

    data = request.get_json()
    name = data.get('name')
    director = data.get('director')
    popularity = data.get('popularity')
    imdb_score = data.get('imdb_score')
    genre_list = data.get('genre', [])

    new_movie = Movie(
        name=name,
        director=director,
        popularity=popularity,
        imdb_score=imdb_score
    )
    new_movie.set_genre(genre_list)

    db_session.add(new_movie)
    db_session.commit()

    # Log the movie addition here (if needed)
    log = MoviesLog(movie_id=new_movie.id, movie_name=new_movie.name, action='ADDED')
    db_session.add(log)
    db_session.commit()
    
    return jsonify(message='Movie added successfully!'), 201

# only admin can access
@api_bp.route('/movies/<int:movie_id>', methods=['PUT', 'DELETE', 'GET'])
@token_required
def manage_movie(movie_id):
    if not g.user.admin:
        return jsonify(message='Admin privilege required'), 403
    
    movie = db_session.get(Movie, movie_id)
    movieID = movie.id
    movieName = movie.name
    if request.method == 'GET':
        if movie:
            return jsonify(movie.serialize())

    if request.method == 'PUT':
        data = request.get_json()
        movie.name = data.get('name', movie.name)
        movie.director = data.get('director', movie.director)
        movie.popularity = data.get('popularity', movie.popularity)
        movie.imdb_score = data.get('imdb_score', movie.imdb_score)
        genre_list = data.get('genre', [])
        movie.set_genre(genre_list)
        db_session.commit()
        # Log the movie update here (if needed)
        log = MoviesLog(movie_id=movie.id, movie_name=movie.name, action='UPDATED')
        db_session.add(log)
        db_session.commit()
        return jsonify(message='Movie updated successfully!'), 200

    if request.method == 'DELETE':
        db_session.query(Genre).filter(Genre.movie_id == movie_id).delete()
        db_session.commit()
        db_session.query(Movie).filter(Movie.id == movie_id).delete()
        db_session.commit()
        # Log the movie deletion here (if needed)
        log = MoviesLog(movie_id=movieID, movie_name=movieName, action='DELETED')
        db_session.add(log)
        db_session.commit()
        return jsonify(message='Movie deleted successfully!'), 200

# Flask route to get movie logs(only admin can access)
@api_bp.route('/movie_logs', methods=['GET'])
@token_required
def get_movie_logs():
    if not g.user.admin:
        return jsonify(message='Admin privilege required'), 403
    # Query movie logs from the database
    logs = db_session.query(MoviesLog).all()

    # Serialize the logs
    logs_list = []
    for log in logs:
        logs_list.append({
            'id': log.id,
            'movie_id': log.movie_id,
            'movie_name': log.movie_name,
            'action': log.action,
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'logs': logs_list}), 200

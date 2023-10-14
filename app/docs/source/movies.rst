Movie API
=========

.. automodule:: app.routes.movies
    :members:

Get Movies
----------

.. http:get:: /api/get_movies

    Retrieves a list of movies based on specified filters and search query.

    :query page: The page number of the movie list to retrieve (default: 1).
    :query genre: The genre of the movies to filter by (default: '').
    :query sort: The field to sort the movies by ('imdb_score' or 'popularity', default: 'imdb_score').
    :query order: The order to sort the movies in ('asc' or 'desc', default: 'asc').
    :query search: The search query to filter movies by name or director (default: '').

    :statuscode 200: Successful retrieval. Returns a JSON object with movies and total_pages.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.

Get Genres
----------

.. http:get:: /api/get_genres

    Get the list of all genres.

    :statuscode 200: Successful retrieval. Returns a JSON object with unique genres.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.

Add Movie
---------

.. http:post:: /api/movies

    Adds a new movie to the database.

    :reqheader Authorization: Bearer <your_auth_token>
    :request body: JSON object with movie details.
    :statuscode 201: Movie added successfully.
    :statuscode 400: Bad request. Invalid or missing parameters in the request body.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.
    :statuscode 403: Forbidden. User does not have admin privilege.

Manage Movie
------------

.. http:get:: /api/movies/{movie_id}

    Get details of a movie by its ID.

    :param movie_id: The ID of the movie to retrieve.
    :statuscode 200: Successful retrieval. Returns a JSON object with movie details.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.
    :statuscode 404: Movie not found.

.. http:put:: /api/movies/{movie_id}

    Update a movie by its ID.

    :param movie_id: The ID of the movie to update.
    :reqheader Authorization: Bearer <your_auth_token>
    :request body: JSON object with updated movie details.
    :statuscode 200: Successful update. Returns a JSON object with a success message.
    :statuscode 400: Bad request. Invalid or missing parameters in the request body.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.
    :statuscode 403: Forbidden. User does not have admin privilege.
    :statuscode 404: Movie not found.

.. http:delete:: /api/movies/{movie_id}

    Delete a movie by its ID.

    :param movie_id: The ID of the movie to delete.
    :reqheader Authorization: Bearer <your_auth_token>
    :statuscode 204: Successful deletion. No content returned.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.
    :statuscode 403: Forbidden. User does not have admin privilege.
    :statuscode 404: Movie not found.

Get Movie Logs
--------------

.. http:get:: /api/movie_logs

    Get movie logs from the database.

    :reqheader Authorization: Bearer <your_auth_token>
    :statuscode 200: Successful retrieval. Returns a JSON object with serialized movie logs.
    :statuscode 401: Unauthorized. Missing or invalid authentication token.
    :statuscode 403: Forbidden. User does not have admin privilege.

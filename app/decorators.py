from functools import wraps
from flask import current_app, jsonify, redirect, request, g
from app.models import User
from app.database import get_db

db_session = get_db()

# Decorator function to protect routes with JWT authentication
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_app.testing:
            auth_token = request.headers.get('Authorization')
            if auth_token:
                auth_token = auth_token.split(" ")[1]  # Extract the token part from the header
        else:
            auth_token = request.cookies.get('auth_token')
        if not auth_token:
            return redirect('/login?error=Token is missing', code=401)  # Redirect to login page with error message and 401 Unauthorized code

        # Validate the auth token here 
        user_id = User.decode_auth_token(auth_token)
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            return redirect('/login?error=Invalid token', code=401)  # Redirect to login page with error message and 401 Unauthorized code
        else:
            g.user = user

        return f(*args, **kwargs)

    return decorated_function

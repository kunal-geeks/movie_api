from functools import wraps
from flask import current_app, redirect, request, g
from app.models import User
from app.database import get_db

db_session = get_db()

# Decorator function to protect routes with JWT authentication
def token_required(f):
    """
    Decorator function that validates an authentication token before executing the decorated function.
    
    Args:
        f (function): The function to be decorated.
    
    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Decorator function that adds authentication to a route.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the decorated function.

        Raises:
            Redirect: If the authentication token is missing or invalid.

        """
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


def get_db():
    """
    This is a mock function for get_db().
    """
    pass


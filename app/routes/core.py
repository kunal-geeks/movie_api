from flask import Blueprint, g, jsonify, render_template, request
from app.decorators import token_required
from app.database import get_db

db_session = get_db()

core_bp = Blueprint('core', __name__, url_prefix='')

@core_bp.route('/')
def index():
    """
    Route decorator for the index endpoint.
    
    Returns:
        The rendered 'index.html' template.
    """
    return render_template('index.html')

@core_bp.route('/login')
def login():
    """
    A function that handles the '/login' route.

    Returns:
        A rendered template for the 'login.html' page.
    """
    return render_template('login.html')

@core_bp.route('/register')
def register():
    """
    Register route that renders the 'register.html' template.

    :return: The rendered 'register.html' template.
    """
    return render_template('register.html')

@core_bp.route('/dashboard')
@token_required
def dashboard():
    """
    Render the dashboard page based on user authentication and admin status.

    Returns:
        render_template: The rendered template for the dashboard page.
    """
    # Check user authentication and admin status
    if g.user.admin:
        return render_template('admin_dashboard.html', admin_name=g.user.name), 200  # Render admin dashboard for authenticated admin users
    else:
        return render_template('user_dashboard.html',  user_name=g.user.name), 200
    
@core_bp.route('/edit-account', methods=['GET', 'PUT'], endpoint = 'edit-account')
@token_required
def edit_account():
    """
    Route for editing the user's account information.
    
    This route is accessible through a GET or PUT request to '/edit-account'.
    The function is decorated with the 'token_required' decorator to ensure
    authentication.
    
    Parameters:
    None
    
    Returns:
    For a GET request:
        - Renders the 'edit_account.html' template with the user's name and email
        - Returns a 200 status code
        
    For a PUT request:
        - Retrieves the authenticated user from the token
        - Updates the user's password if a new password is provided
        - Returns a JSON response with a success or fail status and a message
        - Returns a 200 status code for a successful update
        - Returns a 400 status code if a new password is required but not provided
        - Returns a 500 status code for any other exception during the update process
    """
    if request.method == 'GET':
        # Retrieve user's name and email for display
        user = g.user
        data = {
            'name': user.name,
            'email': user.email
        }
        return render_template('edit_account.html', data=data), 200
    elif request.method == 'PUT':
        try:
            user = g.user  # Get the authenticated user from the token
            data = request.get_json()
            new_password = data.get('new_password')
            print(new_password)
            if new_password:
                user.password = user._hash_password(new_password)  # Hash the new password
                db_session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Password updated successfully.'
                }
                return jsonify(responseObject), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'New password is required.'
                }
                return jsonify(responseObject), 400

        except Exception as e:
            db_session.rollback()
            responseObject = {
                'status': 'fail',
                'message': 'Failed to update password. Please try again.'
            }
            return jsonify(responseObject), 500

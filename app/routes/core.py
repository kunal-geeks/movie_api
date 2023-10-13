from flask import Blueprint, g, jsonify, render_template, request
from app.decorators import token_required
from app.database import get_db

db_session = get_db()

core_bp = Blueprint('core', __name__, url_prefix='')

@core_bp.route('/')
def index():
    return render_template('index.html')

@core_bp.route('/login')
def login():
    return render_template('login.html')

@core_bp.route('/register')
def register():
    return render_template('register.html')

@core_bp.route('/dashboard')
@token_required
def dashboard():
    # Check user authentication and admin status
    if g.user.admin:
        return render_template('admin_dashboard.html', admin_name=g.user.name), 200  # Render admin dashboard for authenticated admin users
    else:
        return render_template('user_dashboard.html',  user_name=g.user.name), 200
    
@core_bp.route('/edit-account', methods=['GET', 'PUT'], endpoint = 'edit-account')
@token_required
def edit_account():
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

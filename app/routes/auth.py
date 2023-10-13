from flask import Blueprint, current_app, make_response, request, jsonify, render_template
from app.decorators import token_required
from app.mail_utils import validate_email
from app.models import BlacklistToken, User
from app.database import get_db
from functools import wraps
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

db_session = get_db()

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # get the post data
        if current_app.testing:
            post_data = request.get_json()
        else:
            post_data = request.form
        if validate_email(post_data.get('email')) is False:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid email address.'
            }
            return make_response(jsonify(responseObject)), 400
        try:
            # check if user already exists
            user = db_session.query(User).filter_by(email=post_data.get('email')).first()

            if not user:
                user = User(
                    name=post_data.get('name'),
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    admin=False,
                )
                # insert the user
                db_session.add(user)
                db_session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201

            elif user.check_password(post_data.get('password')):
                responseObject = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return make_response(jsonify(responseObject)), 202

            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Email address is already registered. Please use a different email.',
                }
                return make_response(jsonify(responseObject)), 400

        except Exception as e:
            db_session.rollback()  # Rollback the transaction
            print(str(e))  # Print the exception details for debugging
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500
    else:
        return render_template('register.html'), 200

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the post data
        if current_app.testing:
            post_data = request.get_json()
        else:
            post_data = request.form
        try:
            # fetch the user data
            user = db_session.query(User).filter_by(email=post_data.get('email')).first()
            if user and user.check_password(post_data.get('password')):
                # generate the auth token
                if(current_app.testing):
                    auth_token = user.encode_auth_token(expires_in=5)
                else:
                    auth_token = user.encode_auth_token(expires_in=86400)  #token expiry time set to 24 hours (86400 seconds)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token,
                    }
                    # Set the auth token in a cookie and return the response
                    response = make_response(jsonify(responseObject), 200)
                    response.set_cookie('auth_token', auth_token, secure=True, httponly=True)
                    return response
            elif user:
                responseObject = {
                    'status': 'fail',
                    'message': 'Incorrect password.'
                }
                return make_response(jsonify(responseObject)), 400
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            db_session.rollback()  # Rollback the transaction
            print(str(e))  # Print the exception details for debugging
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500
    else:
        return render_template('login.html'), 200

@auth_bp.route('/status', methods=['GET'])
def status():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(" ")[1]
    else:
        access_token = ''
    if access_token:
        resp = User.decode_auth_token(access_token)
        if not isinstance(resp, str):
            user = db_session.query(User).filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'username': user.name,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401
    
def blacklist_token(auth_token):
    try:
        blacklist_token = BlacklistToken(token=auth_token)
        db_session.add(blacklist_token)
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        print(str(e))
        return False

def clear_auth_cookie(response, domain):
    response.delete_cookie('auth_token', domain=domain)
    return response

def perform_logout(auth_token, testing=False):
    try:
        if not auth_token:
            return {'message': 'No valid auth token found'}, 401
        
        if not testing:
            is_blacklisted = blacklist_token(auth_token)
            if not is_blacklisted:
                return {'message': 'Failed to blacklist the token'}, 500

        response_data = {'message': 'Successfully logged out'}
        status_code = 200
        return response_data, status_code
    except Exception as e:
        print(str(e))
        return {'message': 'An error occurred while processing your request'}, 500

@auth_bp.route('/logout', methods=['POST'], endpoint='logout')
@token_required
def logout():
    try:
        if current_app.testing:
            auth_token = request.headers.get('Authorization')
            auth_token = auth_token.split(" ")[1]  # Extract the token part from the header
        else:
            auth_token = request.cookies.get('auth_token')
        response_data, status_code = perform_logout(auth_token, current_app.testing)
        response = make_response(jsonify(response_data), status_code)
        if status_code == 200:
            response = clear_auth_cookie(response, current_app.config.get('COOKIE_DOMAIN'))
        return response
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'An error occurred while processing your request'}), 500

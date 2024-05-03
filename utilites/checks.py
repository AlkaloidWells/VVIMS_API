from functools import wraps
from flask import abort
from model.models import User  # Import your User model here
from flask_jwt_extended import  get_jwt_identity
from constants.http_status_codes import HTTP_403_FORBIDDEN
from flask import  jsonify

def role_allowed(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the user ID from the current request
            user_id = get_jwt_identity()

            # Retrieve the user from the database based on the user ID
            user = User.query.get(user_id)

            # Check if the user exists and has one of the required roles
            if user and user.user_role in roles:
                # User has one of the required roles, proceed with the function
                return f(*args, **kwargs)
                r
            else:
                # User does not have any of the required roles, abort with 403 Forbidden error
                return jsonify({'message': 'You not Authorized to perform this action'}), HTTP_403_FORBIDDEN

        return decorated_function
    return decorator

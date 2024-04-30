from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user has any of the required roles
            if not any(current_user.has_role(role) for role in roles):
                # Abort with 403 Forbidden error if user does not have any of the required roles
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
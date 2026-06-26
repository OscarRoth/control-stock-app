from functools import wraps

from flask import abort

from flask_login import current_user


def require_role(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if current_user.role not in roles:

                if current_user.role not in roles:
                    abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator
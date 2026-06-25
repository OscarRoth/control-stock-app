from functools import wraps

from flask import flash
from flask import redirect
from flask import url_for

from flask_login import current_user


def require_role(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if current_user.role not in roles:

                flash(
                    "No posee permisos para acceder a esta funcionalidad.",
                    "warning"
                )

                return redirect(url_for("main.home"))

            return func(*args, **kwargs)

        return wrapper

    return decorator
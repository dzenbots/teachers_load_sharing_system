from functools import wraps

from flask import session, url_for
from werkzeug.utils import redirect


def check_user_valid(original_function):

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if 'valid_user' in session:
            return original_function(*args, **kwargs)
        return redirect(url_for('main.index'))

    return wrapper

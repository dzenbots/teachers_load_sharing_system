from functools import wraps

from flask import Flask, session, url_for
from werkzeug.utils import redirect

from login_app import login_app

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.register_blueprint(login_app)


def check_user_valid(original_function):
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if 'valid_user' in session:
            return original_function(*args, **kwargs)
        return redirect(url_for('login_app.login'))

    return wrapper


from index import views

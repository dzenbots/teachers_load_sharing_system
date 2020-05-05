from functools import wraps

from flask import Blueprint, session, render_template, url_for
from werkzeug.utils import redirect

from app.models import initialize_db, db


def check_user_valid(original_function):

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if 'valid_user' in session:
            return original_function(*args, **kwargs)
        return redirect(url_for('login_app.login'))

    return wrapper


main = Blueprint('main', __name__)


@main.before_request
def before_request():
    initialize_db()


@main.teardown_request
def after_request(exception):
    db.close()


@main.errorhandler(404)
def http_404_handler(error):
    return render_template('404_error.html')


@main.route("/")
@main.route("/index")
@check_user_valid
def index():
    return render_template('main_app.html')

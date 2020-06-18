from functools import wraps

from flask import Blueprint, session, url_for, render_template
from werkzeug.utils import redirect


def check_user_valid(original_function):

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if 'valid_user' in session:
            return original_function(*args, **kwargs)
        return redirect(url_for('login_app.login'))

    return wrapper


main = Blueprint('main', __name__, url_prefix='', static_folder='static',
                        template_folder='templates')


@main.errorhandler(404)
def http_404_handler(error):
    return render_template('404_error.html')


@main.route("/")
@main.route("/index")
@check_user_valid
def index():
    return render_template('main_app.html')

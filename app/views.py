from flask import Blueprint, session, render_template, url_for
from werkzeug.utils import redirect

from .models import initialize_db
from .models import db

main = Blueprint('main', __name__)


def check_user_valid():
    if 'valid_user' in session:
        return session.get('valid_user')
    return False


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
def index():
    if check_user_valid():
        return render_template('main_app.html')
    else:
        return redirect(url_for('login_app.login'))

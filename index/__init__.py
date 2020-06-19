from functools import wraps

from flask import Flask, session, url_for
from werkzeug.utils import redirect

from login_app import login_app

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.register_blueprint(login_app)

from index import views

from flask import Blueprint, render_template
from .models import db, initialize_db

main = Blueprint('main', __name__,  static_folder="static", template_folder="templates")


@main.before_request
def before_request():
    initialize_db()


@main.teardown_request
def after_request(exception):
    db.close()


@main.route('/')
def main_index():
    return 'Blueprint hello!'

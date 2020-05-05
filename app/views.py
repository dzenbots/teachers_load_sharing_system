from flask import Blueprint
from .models import initialize_db

main = Blueprint('main', __name__)


@main.before_request
def before_request():
    initialize_db()


@main.route('/')
def main_index():
    return 'Blueprint hello!'

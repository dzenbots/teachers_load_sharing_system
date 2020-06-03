from flask import Blueprint

from app.itog_nagruzka_app import check_user_valid
from app.itog_nagruzka_app.models import initialize_db, db

nagruzka_app = Blueprint('nagruzka_app',
                         __name__,
                         static_folder='static',
                         template_folder='templates',
                         url_prefix='/nagruzka_app')


@nagruzka_app.before_request
@check_user_valid
def classes_before_request():
    initialize_db()


@nagruzka_app.after_request
def classes_after_request(resp):
    db.close()
    return resp


@nagruzka_app.teardown_request
def classes_teardown_request(exception):
    db.close()


@check_user_valid
@nagruzka_app.route('/')
def show_all():
    pass

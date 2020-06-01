from flask import Blueprint

from app.metagroupes_app import check_user_valid
from app.metagroupes_app.models import initialize_db, db

metagroupes_app = Blueprint('metagroupes_app',
                            __name__,
                            static_folder='static',
                            template_folder='templates',
                            url_prefix='/metagroupes_app')


@metagroupes_app.before_request
@check_user_valid
def classes_before_request():
    initialize_db()


@metagroupes_app.after_request
def classes_after_request(resp):
    db.close()
    return resp


@metagroupes_app.teardown_request
def classes_teardown_request(exception):
    db.close()


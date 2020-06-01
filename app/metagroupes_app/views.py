from flask import Blueprint, render_template

from app.metagroupes_app import check_user_valid
from app.metagroupes_app.models import initialize_db, db, Subjects, Parallels, ClassesSubjects

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


@check_user_valid
@metagroupes_app.route('/<parallel>')
def show_parallel(parallel):
    data = dict()
    data['subjects'] = Subjects.select().order_by(Subjects.name)
    data['classes'] = Parallels.get(name=parallel).parallel_classes
    data['meta'] = []
    for klass in data.get('classes'):
        data['meta'].append(klass.class_metagroups)
    return render_template("metagroupes_app.html",
                           parallel=parallel,
                           data=data)

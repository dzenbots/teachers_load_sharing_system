from flask import Blueprint, render_template

from app.metagroupes_app import check_user_valid
from app.metagroupes_app.models import initialize_db, db, Subjects, Parallels

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
    for klass in Parallels.get(name=parallel).parallel_classes:
        data[klass.name] = dict()
        for metagroup in klass.class_metagroups:
            data[klass.name][f"{metagroup.id}"] = {'subject': Subjects.get(id=metagroup.subject_name).name,
                                                   'meta_name': metagroup.meta_name}
    return render_template("metagroupes_app.html",
                           parallel=parallel,
                           data=data)

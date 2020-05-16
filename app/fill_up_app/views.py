from flask import Blueprint, render_template

from app.fill_up_app import check_user_valid
from app.fill_up_app.models import initialize_db, db, Subjects, Parallels, ClassesSubjects

fill_up_app = Blueprint('fill_up_app',
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/fill_up_app')


@fill_up_app.before_request
@check_user_valid
def classes_before_request():
    initialize_db()


@fill_up_app.after_request
def classes_after_request(resp):
    db.close()
    return resp


@fill_up_app.teardown_request
def classes_teardown_request(exception):
    db.close()


@check_user_valid
@fill_up_app.route('/<parallel>')
def show_parallel(parallel):
    data = dict()
    data['subjects'] = Subjects.select().order_by(Subjects.name)
    data['classes'] = Parallels.get(name=parallel).parallel_classes
    data['links'] = ClassesSubjects.select()
    return render_template("fill_up_app.html",
                           parallel=parallel,
                           data=data)

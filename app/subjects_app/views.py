from flask import Blueprint, render_template, url_for, request, redirect, Response

from app.subjects_app import subjects_table_head, check_user_valid
from app.subjects_app.models import Subjects, initialize_db, close_db

subjects_app = Blueprint('subjects_app', __name__,
                         static_folder='static',
                         template_folder='templates',
                         url_prefix='/subjects_app')


@subjects_app.before_request
@check_user_valid
def subjects_before_request():
    initialize_db()


@subjects_app.after_request
def subjects_before_request(resp):
    close_db()
    return resp


@subjects_app.teardown_request
def classes_teardown_request(exception):
    close_db()


@subjects_app.route('/')
def show_subjects():
    return render_template('subjects_app.html',
                           table_info=subjects_table_head,
                           subjects=Subjects.select().order_by(Subjects.name))


@subjects_app.route('/add_new_record', methods=['POST'])
def add_new_subject():
    Subjects.get_or_create(name=request.form.get('subject_add_new'))
    return redirect(url_for('subjects_app.show_subjects'))


@subjects_app.route('/update_record/<record_id>', methods=['POST'])
def update_db_record(record_id):
    if not (request.form.get(f'id_{record_id}') == ""):
        if Subjects.select().where(Subjects.name == request.form.get(f'id_{record_id}')).count() == 0:
            Subjects.update(name=request.form.get(f'id_{record_id}')).where(Subjects.id == record_id).execute()
    return Response(status=200)

from flask import Blueprint, render_template, url_for, session, request, redirect, Response

from app.models import Subjects
from app.subjects_app import subjects_table_head, check_user_valid

subjects_app = Blueprint('subjects_app', __name__,
                         static_folder='static',
                         template_folder='templates',
                         url_prefix='/subjects_app')


@subjects_app.route('/')
@check_user_valid
def show_subjects():
    return render_template('subjects_app.html',
                           table_info=subjects_table_head,
                           subjects=Subjects.select().order_by(Subjects.name))


@subjects_app.route('/add_new_record', methods=['POST'])
@check_user_valid
def add_new_subject():
    Subjects.create(name=request.form.get('subject_add_new'))
    return redirect(url_for('subjects_app.show_subjects'))


@subjects_app.route('/update_record/<record_id>', methods=['POST'])
@check_user_valid
def update_db_record(record_id):
    Subjects.update(name=request.form.get(f'id_{record_id}')).where(Subjects.id == record_id).execute()
    return Response(status=200)

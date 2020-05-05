from flask import Blueprint, render_template, url_for, session, request, redirect, Response

from app.models import Subjects
from app.subjects_app import subjects_table_head

subjects_app = Blueprint('subjects_app', __name__,
                         static_folder='static',
                         template_folder='templates',
                         url_prefix='/subjects_app')


def check_user_valid():
    if 'valid_user' in session:
        return session.get('valid_user')
    return False


@subjects_app.route('/')
def show_subjects():
    if check_user_valid():
        return render_template('subjects_app.html',
                               table_info=subjects_table_head,
                               subjects=Subjects.select().order_by(Subjects.name))
    else:
        return redirect(url_for('index'))


@subjects_app.route('/add_new_record', methods=['POST'])
def add_new_subject():
    if check_user_valid():
        Subjects.create(name=request.form.get('subject_add_new'))
        return redirect(url_for('subjects_app.show_subjects'))
    else:
        return redirect(url_for('index'))


@subjects_app.route('/update_record/<record_id>', methods=['POST'])
def update_db_record(record_id):
    if check_user_valid():
        Subjects.update(name=request.form.get(f'id_{record_id}')).where(Subjects.id == record_id).execute()
        response = Response(status=200)
    else:
        response = Response(status=304)
    return response

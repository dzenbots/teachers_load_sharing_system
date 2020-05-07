from flask import Blueprint, render_template, url_for, session, request, redirect, Response

from app.classes_app import classes_table_head, classes_row_table_head, classes_levels
from app.models import Classes

classes_app = Blueprint('classes_app', __name__, static_folder='static', template_folder='templates')


def check_user_valid():
    if 'valid_user' in session:
        return session.get('valid_user')
    return False


@classes_app.route('/')
def show_classes():
    if check_user_valid():
        return render_template('classes_app.html',
                               table_info=classes_table_head,
                               row_table_info=classes_row_table_head,
                               data_HOO=Classes
                               .select()
                               .where(Classes.level == classes_levels.get('HOO'))
                               .order_by(Classes.name),
                               data_OOO=Classes
                               .select()
                               .where(Classes.level == classes_levels.get('OOO'))
                               .order_by(Classes.name),
                               data_COO=Classes
                               .select()
                               .where(Classes.level == classes_levels.get('COO'))
                               .order_by(Classes.name)
                               )
    else:
        return redirect(url_for('index'))


@classes_app.route('/add_new_record', methods=['POST'])
def add_new_class():
    if check_user_valid():
        Classes.create(name=request.form.get('ClassName'),
                       level=request.form.get('Level'),
                       parallel=request.form.get('Parallel'))
        return redirect(url_for('classes_app.show_classes'))
    else:
        return redirect(url_for('index'))


@classes_app.route('/update_record/<record_id>', methods=['POST'])
def update_db_record(record_id):
    if check_user_valid():
        Classes.update(name=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[1])),
                       parallel=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[2])),
                       level=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[3])))\
            .where(Classes.id == record_id).execute()
        response = Response(status=200)
    else:
        response = Response(status=304)
    return response

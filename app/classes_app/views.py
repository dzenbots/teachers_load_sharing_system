from flask import Blueprint, render_template, url_for, request, redirect, Response

from app.classes_app import classes_table_head, classes_row_table_head, check_user_valid, classes_levels
from app.models import Classes, Parallels, StudyLevels

classes_app = Blueprint('classes_app',
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/classes_app')


@classes_app.route('/')
@check_user_valid
def show_classes():
    noo_classes = Classes.select().join(Parallels).join(StudyLevels).where(
        StudyLevels.name == classes_levels.get('HOO'))
    ooo_classes = Classes.select().join(Parallels).join(StudyLevels).where(
        StudyLevels.name == classes_levels.get('OOO'))
    coo_classes = Classes.select().join(Parallels).join(StudyLevels).where(
        StudyLevels.name == classes_levels.get('COO'))
    return render_template('classes_app.html',
                           table_info=classes_table_head,
                           row_table_info=classes_row_table_head,
                           data_HOO=noo_classes,
                           data_OOO=ooo_classes,
                           data_COO=coo_classes
                           )


@classes_app.route('/add_new_class', methods=['POST'])
@check_user_valid
def add_new_class():
    Classes.create(name=request.form.get('ClassName'),
                   parallel=Parallels.select().where(Parallels.name == request.form.get('Parallel')),
                   max_hours=request.form.get('max_hours'),
                   students_num=request.form.get('students_num'))
    return redirect(url_for('classes_app.show_classes'))


@classes_app.route('/update_class/<record_id>', methods=['POST'])
@check_user_valid
def update_db_record(record_id):
    Classes.update(name=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[1])),
                   parallel=Parallels.select().where(Parallels.name == request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[2]))),
                   max_hours=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[3])),
                   students_num=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[4]))) \
        .where(Classes.id == record_id).execute()
    return Response(status=200)

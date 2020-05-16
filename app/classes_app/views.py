from flask import Blueprint, render_template, url_for, request, redirect, Response

from app.classes_app import classes_table_head, classes_row_table_head, check_user_valid, classes_levels
from app.classes_app.models import Classes, Parallels, StudyLevels, db, initialize_db

classes_app = Blueprint('classes_app',
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/classes_app')


@classes_app.before_request
@check_user_valid
def classes_before_request():
    initialize_db()


@classes_app.after_request
def classes_after_request(resp):
    db.close()
    return resp


@classes_app.teardown_request
def classes_teardown_request(exception):
    db.close()


@classes_app.route('/')
def show_classes():
    noo_classes = []
    ooo_classes = []
    coo_classes = []

    for parallel in StudyLevels.get(StudyLevels.name == classes_levels.get('HOO')).level_parallels:
        for noo_class in parallel.classes_parallel:
            noo_classes.append(noo_class)

    for parallel in StudyLevels.get(StudyLevels.name == classes_levels.get('OOO')).level_parallels:
        for ooo_class in parallel.classes_parallel:
            ooo_classes.append(ooo_class)

    for parallel in StudyLevels.get(StudyLevels.name == classes_levels.get('COO')).level_parallels:
        for coo_class in parallel.classes_parallel:
            coo_classes.append(coo_class)

    return render_template('classes_app.html',
                           table_info=classes_table_head,
                           row_table_info=classes_row_table_head,
                           data_HOO=noo_classes,
                           data_OOO=ooo_classes,
                           data_COO=coo_classes
                           )


@classes_app.route('/add_new_class', methods=['POST'])
def add_new_class():
    Classes.get_or_create(name=request.form.get('ClassName'),
                          parallel=Parallels.get(name=request.form.get('Parallel')),
                          hours_num=0,
                          students_num=request.form.get('students_num'))
    return redirect(url_for('classes_app.show_classes'))


@classes_app.route('/update_class/<record_id>', methods=['POST'])
def update_db_record(record_id):
    if request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[1])) == "":
        return Response(status=200)
    elif Classes.select().where(
            Classes.name == request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[1]))).count() > 1:
        return Response(status=200)
    else:
        Classes.update(name=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[1])),
                       parallel=Parallels.select().where(
                           Parallels.name == request.form.get(
                               'id_{}_{}'.format(record_id, classes_row_table_head[2]))),
                       students_num=request.form.get('id_{}_{}'.format(record_id, classes_row_table_head[3]))) \
            .where(Classes.id == record_id).execute()
        return Response(status=200)

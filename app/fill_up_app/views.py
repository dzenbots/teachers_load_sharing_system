from flask import Blueprint, render_template, Response, request

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
    data['links'] = {}
    ClassesSubjects.select().where(ClassesSubjects.class_id == data['classes'])
    for klass in data['classes']:
        for row in ClassesSubjects.select().where(ClassesSubjects.class_id == klass):
            data['links'][f"{row.class_id}_{row.subject_name}"] = {
                "hours_num": row.hours_num,
                "groups_num": row.groups_num
            }
    return render_template("fill_up_app.html",
                           parallel=parallel,
                           data=data)


@check_user_valid
@fill_up_app.route('/save_changes/<parallel>', methods=['POST'])
def save_changes(parallel):
    data = dict()
    data['subjects'] = Subjects.select().order_by(Subjects.name)
    data['classes'] = Parallels.get(name=parallel).parallel_classes
    for subject in data['subjects']:
        for klass in data['classes']:
            if request.form.get('hours_{}_{}'.format(subject.id, klass.id)) != "":
                groups_num = request.form.get('groups_{}_{}'.format(subject.id, klass.id))
                hours_num = request.form.get('hours_{}_{}'.format(subject.id, klass.id))
                selection = ClassesSubjects.select() \
                    .where(ClassesSubjects.class_id == klass) \
                    .where(ClassesSubjects.subject_name == subject)
                if selection.count() == 0:
                    ClassesSubjects.create(class_id=klass,
                                           subject_name=subject,
                                           groups_num=groups_num,
                                           hours_num=hours_num)
                elif selection.count() == 1:
                    ClassesSubjects.update(groups_num=groups_num, hours_num=hours_num) \
                        .where(ClassesSubjects.class_id == klass) \
                        .where(ClassesSubjects.subject_name == subject).execute()
    return Response(status=200)

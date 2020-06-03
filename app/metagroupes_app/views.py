from flask import Blueprint, render_template, request, Response

from app.metagroupes_app import check_user_valid
from app.metagroupes_app.models import initialize_db, db, Subjects, Parallels, Metagroups, Classes, Nagruzka

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


@check_user_valid
@metagroupes_app.route('/save_changes/<parallel>', methods=['POST'])
def save_changes(parallel):
    for klass in Parallels.get(name=parallel).parallel_classes:
        for metagroup in klass.class_metagroups:
            meta_name = request.form.get(f'meta_{metagroup.id}')
            Metagroups.update({Metagroups.meta_name: meta_name}) \
                .where(Metagroups.id == metagroup.id) \
                .execute()

    meta_data = dict()
    for metagroup in Metagroups.select():
        if not (Subjects.get(id=metagroup.subject_name).name in meta_data):
            meta_data[Subjects.get(id=metagroup.subject_name).name] = dict()

        if not (metagroup.meta_name in meta_data[Subjects.get(id=metagroup.subject_name).name]):
            meta_data[Subjects.get(id=metagroup.subject_name).name][metagroup.meta_name] = dict()
            meta_data[Subjects.get(id=metagroup.subject_name).name][metagroup.meta_name]['classes'] = Classes.get(
                id=metagroup.class_id).name
        else:
            meta_data[Subjects.get(id=metagroup.subject_name).name][metagroup.meta_name]['classes'] += \
                f"_{Classes.get(id=metagroup.class_id).name}"
    # for subject, metagroup in meta_data.items():
    #     print(subject, metagroup)

    nagruzka = []

    for subject, groups in meta_data.items():
        for meta_name, group in groups.items():
            nagruzka.append({
                'subject': subject,
                'meta_name': meta_name,
                'classes': group.get('classes')
            })
    for item in nagruzka:
        print(item)
        # if Nagruzka.select().where(Nagruzka.meta_name == item.get('meta_name')).where(Nagruzka.subject_name == item.get('subject')):
    return Response(status=200)

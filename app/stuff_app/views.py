from flask import Blueprint, render_template, redirect, url_for, request, Response

from app.stuff_app import check_user_valid
from app.stuff_app.models import initialize_db, db, Stuff, StuffSubject
from app.subjects_app import Subjects

stuff_app = Blueprint('stuff_app',
                      __name__,
                      static_folder='static',
                      template_folder='templates',
                      url_prefix='/stuff_app')


@stuff_app.before_request
@check_user_valid
def classes_before_request():
    initialize_db()


@stuff_app.after_request
def classes_after_request(resp):
    db.close()
    return resp


@stuff_app.teardown_request
def classes_teardown_request(exception):
    db.close()


@stuff_app.route("/")
def show_stuff():
    links = dict()
    for person in Stuff.select():
        links[person.id] = []
        for item in person.stuff_subject:
            subject = item.subject
            links[person.id].append(subject.id)
    return render_template("stuff_app.html",
                           subjects=Subjects.select().order_by(Subjects.name),
                           persons=Stuff.select().order_by(Stuff.name),
                           links=links
                           )


@stuff_app.route("/add_new_person", methods=['POST'])
def add_stuff():
    Stuff.get_or_create(name=request.form.get('StuffName'))
    return redirect(url_for('stuff_app.show_stuff'))


@stuff_app.route('/checkbox_check/<person_id>/<subject_id>', methods=['POST'])
def subject_to_person(person_id, subject_id):
    if f'check_box_{person_id}_{subject_id}' in request.form:
        StuffSubject.get_or_create(stuff=person_id, subject=subject_id)
    elif not (f"check_box_{person_id}_{subject_id}" in request.form):
        StuffSubject.delete().where(StuffSubject.stuff == person_id).where(StuffSubject.subject == subject_id).execute()
    return Response(status=200)

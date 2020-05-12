from flask import Blueprint, render_template, redirect, url_for, session, request, Response
from models import PersonSubject, Persons, Subjects

stuff_app = Blueprint('stuff_app', __name__, static_folder='static', template_folder='templates')

def check_user_valid():
    if 'valid_user' in session:
        return session.get('valid_user')
    return False


@stuff_app.route("/")
def show_stuff():
    if check_user_valid():
        stuff_data = {
            "stuff": Persons.select().order_by(Persons.name),
            "subjects": Subjects.select().order_by(Subjects.name),
            "links": dict()
        }
        for person in stuff_data.get("stuff"):
            stuff_data.get("links")[person.id] = []
            for item in PersonSubject.select(PersonSubject.SubjectId).where(PersonSubject.PersonId == person.id).dicts():
                stuff_data.get("links")[person.id].append(item.get('SubjectId'))
        return render_template("stuff_app.html", data=stuff_data)
    else:
        return redirect(url_for('index'))


@stuff_app.route("/add_new_person", methods=['POST'])
def add_stuff():
    if check_user_valid():
        Persons.create(name=request.form.get('StuffName'))
        return redirect(url_for('stuff_app.show_stuff'))
    else:
        return redirect(url_for('index'))


@stuff_app.route('/checkbox_check/<person_id>/<subject_id>', methods=['POST'])
def subject_to_person(person_id, subject_id):
    if check_user_valid():
        if f'check_box_{person_id}_{subject_id}' in request.form:
            PersonSubject.create(PersonId=person_id, SubjectId=subject_id)
        elif not (f"check_box_{person_id}_{subject_id}" in request.form):
            PersonSubject.delete().where(PersonSubject.PersonId == person_id and PersonSubject.SubjectId == subject_id).execute()
        response = Response(status=200)
    else:
        response = Response(status=304)
    return response

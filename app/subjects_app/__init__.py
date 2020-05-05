from functools import wraps

from flask import session, url_for
from werkzeug.utils import redirect

from app.models import Subjects, Classes

subject_aliases = {
    "name": "Предметы"
}

classes_aliases = {
    "name": "Название класса",
    "parallel": "Параллель",
    "max_hours": "Макс. часов",
    "students_num": "Количество учеников"
}

classes_levels = {
    "HOO": 'НОО',
    "OOO": 'ООО',
    "COO": 'СОО',
}

subject_row_table_head = Subjects._meta.sorted_field_names
subjects_table_head = []
for field in subject_row_table_head:
    subjects_table_head.append(subject_aliases.get(field))

classes_row_table_head = Classes._meta.sorted_field_names
classes_table_head = []
for field in classes_row_table_head:
    classes_table_head.append(classes_aliases.get(field))


def check_user_valid(original_function):

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if 'valid_user' in session:
            return original_function(*args, **kwargs)
        return redirect(url_for('main.index'))

    return wrapper

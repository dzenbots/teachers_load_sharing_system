from app.models import Classes


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

classes_row_table_head = Classes._meta.sorted_field_names
classes_table_head = []
for field in classes_row_table_head:
    classes_table_head.append(classes_aliases.get(field))

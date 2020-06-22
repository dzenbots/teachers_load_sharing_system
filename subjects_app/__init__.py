from index.models import Subjects

subject_aliases = {
    "name": "Предметы"
}

subject_row_table_head = Subjects._meta.sorted_field_names
subjects_table_head = []
for field in subject_row_table_head:
    subjects_table_head.append(subject_aliases.get(field))

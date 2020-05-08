from peewee import Model, CharField, IntegerField, ForeignKeyField, PrimaryKeyField, SqliteDatabase

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class StudyLevels(BaseModel):
    name = CharField(max_length=255, unique=True)


class Parallels(BaseModel):
    name = IntegerField(unique=True)
    level = ForeignKeyField(StudyLevels, backref="level_parallels")
    max_hours = IntegerField()


class Classes(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=255, unique=True)
    parallel = ForeignKeyField(Parallels, backref="classes_parallel")
    # max_hours = IntegerField()
    students_num = IntegerField()


class Subjects(BaseModel):
    name = CharField()


class Stuff(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    # position = CharField()


class StuffSubject(BaseModel):
    id = PrimaryKeyField()
    stuff_id = ForeignKeyField(Stuff.id)
    subject_name = ForeignKeyField(Subjects.name, backref="subject_stuff")


class ClassesSubjects(BaseModel):
    id = PrimaryKeyField()
    class_id = ForeignKeyField(Classes.id, backref="class_subjects")
    subject_name = ForeignKeyField(Subjects.name, backref="subject_classes")
    groups_num = IntegerField()
    hours_num = IntegerField()


class Metagroups(BaseModel):
    id = PrimaryKeyField()
    class_id = ForeignKeyField(Classes.id, backref="class_metagroups")
    subject_name = ForeignKeyField(Subjects.name, backref="subject_metagroups")
    meta_name = CharField(max_length=255)


class Nagruzka(BaseModel):
    id = PrimaryKeyField()
    subject_name = ForeignKeyField(Subjects.name, backref="subject_metagrops")
    stuff_id = ForeignKeyField(Stuff.id, backref="stuff_nagruzka")
    meta_name = ForeignKeyField(Metagroups.meta_name, backref="meta_nagruzka")


def initialize_db():
    db.connect()
    db.create_tables(
        [
            StudyLevels,
            Parallels,
            Classes,
            Subjects,
            Stuff,
            StuffSubject,
            ClassesSubjects,
            Metagroups,
            Nagruzka
        ], safe=True)
    noo, create = StudyLevels.get_or_create(name='НОО')
    ooo, create = StudyLevels.get_or_create(name='ООО')
    coo, create = StudyLevels.get_or_create(name='СОО')

    Parallels.get_or_create(name=1, max_hours=21, level=noo)
    for i in range(2, 5):
        Parallels.get_or_create(name=i, max_hours=23, level=noo)

    Parallels.get_or_create(name=5, max_hours=29, level=ooo)
    Parallels.get_or_create(name=6, max_hours=30, level=ooo)
    Parallels.get_or_create(name=7, max_hours=32, level=ooo)
    Parallels.get_or_create(name=8, max_hours=33, level=ooo)
    Parallels.get_or_create(name=9, max_hours=33, level=ooo)

    Parallels.get_or_create(name=10, max_hours=34, level=coo)
    Parallels.get_or_create(name=11, max_hours=34, level=coo)

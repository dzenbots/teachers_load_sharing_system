from peewee import Model, CharField, IntegerField, ForeignKeyField, PrimaryKeyField, SqliteDatabase
from .settings import DB_FILE_PATH

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class StudyLevels(BaseModel):
    name = CharField(max_length=255)


class Parallels(BaseModel):
    name = IntegerField()
    level = ForeignKeyField(StudyLevels, backref="level_parallels")


class Classes(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=255)
    parallel = ForeignKeyField(Parallels, backref="classes_parallel")
    max_hours = IntegerField()
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
    noo = StudyLevels.create(name='НОО')
    ooo = StudyLevels.create(name='ООО')
    coo = StudyLevels.create(name='СОО')

    for i in range(1, 5):
        Parallels.insert(name=i, level=noo).execute()
    for i in range(5, 10):
        Parallels.insert(name=i, level=ooo).execute()
    for i in range(10, 12):
        Parallels.insert(name=i, level=coo).execute()

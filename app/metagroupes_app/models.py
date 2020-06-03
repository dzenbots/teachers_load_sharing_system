import os

from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, IntegerField

db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


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
    name = CharField(max_length=255, unique=True)
    parallel = ForeignKeyField(Parallels, backref="parallel_classes")
    students_num = IntegerField()


class Subjects(BaseModel):
    name = CharField(unique=True)


class Stuff(BaseModel):
    name = CharField(unique=True)
    # position = CharField()


class ClassesSubjects(BaseModel):
    class_id = ForeignKeyField(Classes, backref="class_subjects")
    subject_name = ForeignKeyField(Subjects, backref="subject_classes")
    groups_num = IntegerField()
    hours_num = IntegerField()


class Metagroups(BaseModel):
    class_id = ForeignKeyField(Classes, backref="class_metagroups")
    subject_name = ForeignKeyField(Subjects, backref="subject_metagroups")
    meta_name = CharField(max_length=255)


class Nagruzka(BaseModel):
    subject_name = ForeignKeyField(Subjects, backref="subject_metagrops")
    stuff_id = ForeignKeyField(Stuff, backref="stuff_nagruzka", null=False)
    meta_name = ForeignKeyField(Metagroups, backref="meta_nagruzka")
    classes = CharField()


def initialize_db():
    db.connect()
    db.create_tables(
        [
            StudyLevels,
            Parallels,
            Classes,
            Subjects,
            ClassesSubjects,
            Metagroups,
            Nagruzka
        ], safe=True)

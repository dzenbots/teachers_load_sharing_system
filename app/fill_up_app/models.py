import os

from peewee import SqliteDatabase, Model, CharField, PrimaryKeyField, ForeignKeyField, IntegerField

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
    id = PrimaryKeyField()
    name = CharField(max_length=255, unique=True)
    parallel = ForeignKeyField(Parallels, backref="parallel_classes")
    hours_num = IntegerField()
    students_num = IntegerField()


class Subjects(BaseModel):
    name = CharField(unique=True)


class ClassesSubjects(BaseModel):
    id = PrimaryKeyField()
    class_id = ForeignKeyField(Classes, backref="class_subjects")
    subject_name = ForeignKeyField(Subjects, backref="subject_classes")
    groups_num = IntegerField()
    hours_num = IntegerField()


def initialize_db():
    db.connect()
    db.create_tables(
        [
            StudyLevels,
            Parallels,
            Classes,
            Subjects,
            ClassesSubjects
        ], safe=True)


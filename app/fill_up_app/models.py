import os

from peewee import SqliteDatabase, Model, CharField, PrimaryKeyField, ForeignKeyField, IntegerField

db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class StudyLevels(BaseModel):
    name = CharField(max_length=255)


class Parallels(BaseModel):
    name = IntegerField()
    level = ForeignKeyField(StudyLevels.name, backref="level_parallels")


class Classes(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=255)
    parallel = ForeignKeyField(Parallels.name, backref="parallel_classes")
    max_hours = IntegerField()
    students_num = IntegerField()


class Subjects(BaseModel):
    name = CharField()


class ClassesSubjects(BaseModel):
    id = PrimaryKeyField()
    class_id = ForeignKeyField(Classes.id, backref="class_subjects")
    subject_name = ForeignKeyField(Subjects.name, backref="subject_classes")
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


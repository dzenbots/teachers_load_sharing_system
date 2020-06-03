import os

from peewee import SqliteDatabase, Model, PrimaryKeyField, ForeignKeyField, CharField, IntegerField

db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class StudyLevels(BaseModel):
    name = CharField(max_length=255, unique=True)


class Parallels(BaseModel):
    name = IntegerField()
    level = ForeignKeyField(StudyLevels, backref="level_parallels")


class Classes(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=255)
    parallel = ForeignKeyField(Parallels, backref="parallel_classes")
    students_num = IntegerField()


class Subjects(BaseModel):
    name = CharField()


class Stuff(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    # position = CharField()


class Metagroups(BaseModel):
    id = PrimaryKeyField()
    class_id = ForeignKeyField(Classes, backref="class_metagroups")
    subject_name = ForeignKeyField(Subjects, backref="subject_metagroups")
    meta_name = CharField(max_length=255)


class Nagruzka(BaseModel):
    id = PrimaryKeyField()
    subject_name = ForeignKeyField(Subjects, backref="subject_metagrops")
    stuff_id = ForeignKeyField(Stuff, backref="stuff_nagruzka", null=False)
    meta_name = ForeignKeyField(Metagroups, backref="meta_nagruzka")


def initialize_db():
    db.connect()
    db.create_tables(
        [
            StudyLevels,
            Parallels,
            Classes,
            Subjects,
            Metagroups,
            Nagruzka
        ], safe=True)

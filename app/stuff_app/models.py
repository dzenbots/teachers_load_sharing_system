import os

from peewee import SqliteDatabase, Model, PrimaryKeyField, CharField, ForeignKeyField

db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class Subjects(BaseModel):
    name = CharField(unique=True)


class Stuff(BaseModel):
    name = CharField(unique=True)
    # position = CharField()


class StuffSubject(BaseModel):
    stuff = ForeignKeyField(Stuff, backref='stuff_subject')
    subject = ForeignKeyField(Subjects, backref="subject_stuff")


def initialize_db():
    db.connect()
    db.create_tables(
        [
            Stuff,
            StuffSubject,
            Subjects
        ], safe=True)

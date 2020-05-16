import os

from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class Subjects(BaseModel):
    name = CharField(unique=True)


def initialize_db():
    db.connect()
    db.create_tables([Subjects], safe=True)


def close_db():
    db.close()

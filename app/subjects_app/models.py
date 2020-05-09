from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Subjects(BaseModel):
    name = CharField()


def initialize_db():
    db.connect()
    db.create_tables([Subjects], safe=True)
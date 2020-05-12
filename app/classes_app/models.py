import os

from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, PrimaryKeyField

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
    parallel = ForeignKeyField(Parallels, backref="classes_parallel")
    # max_hours = IntegerField()
    students_num = IntegerField()


def initialize_db():
    db.connect()
    db.create_tables(
        [
            StudyLevels,
            Parallels,
            Classes
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

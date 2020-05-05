from peewee import SqliteDatabase
from .settings import DB_FILE_PATH

db = SqliteDatabase(DB_FILE_PATH)


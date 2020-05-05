from peewee import Model
from .extentions import db


class BaseModel(Model):
    class Meta:
        database = db

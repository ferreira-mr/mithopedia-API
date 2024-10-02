from peewee import AutoField, CharField, IntegerField, Model
from config.database import database

class UserDB(Model):
    id = AutoField()
    name = CharField()
    email = CharField()
    password = CharField()
    type = IntegerField()

    class Meta:
        database = database
        table_name = 'user'

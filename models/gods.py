from peewee import AutoField, CharField, FloatField, Model, DateField, IntegerField, ForeignKeyField
from config.database import database

class GodsDB(Model):
    id = AutoField()
    name = CharField()
    sub_description = CharField()
    description = CharField()
    symbol = CharField()
    domain = CharField()
    kinship = CharField()
    caracteristics = CharField()
    sacred_animal = CharField()
    sacred_colour = CharField()
    data_creation = DateField()
    last_update = DateField()

    class Meta:
        database = database
        table_name = 'gods'
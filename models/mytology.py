# models/mytology_history.py
from peewee import AutoField, CharField, FloatField, Model, DateField, IntegerField, ForeignKeyField
from config.database import database
# from models.history import HistoryDB


class MytologyDB(Model):
    id = AutoField()
    name = CharField()
    sub_description = CharField()
    description = CharField()
    origin = CharField()
    period = CharField()
    gods_qty = IntegerField()
    sacred_texts = CharField()
    main_mytology = CharField()
    main_symbol = CharField()  # Path or URL to the image
    mytology_banner = CharField()  # Path or URL to the image
    mytology_profile_img = CharField()  # Path or URL to the image
    creator = CharField()
    data_creation = DateField()
    last_update = DateField()

    class Meta:
        database = database
        table_name = 'mytology'

from peewee import Model, AutoField, CharField, DateTimeField, IntegerField, ForeignKeyField
from config.database import database
from models.mytology import MytologyDB  # Make sure to import MytologyDB
from models.gods import GodsDB


class HistoryDB(Model):
    id = AutoField()
    title = CharField()
    content = CharField()
    author = CharField()
    source = CharField()
    publish_time = DateTimeField()
    last_updated = DateTimeField()
    views = IntegerField()
    age_classification = IntegerField()
    god = ForeignKeyField(model=GodsDB, backref='stories')
    mythology = ForeignKeyField(MytologyDB, backref='stories')  # Define the foreign key relationship

    class Meta:
        database = database
        table_name = 'history'

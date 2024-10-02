from peewee import AutoField, CharField, DateTimeField, IntegerField, ForeignKeyField, Model
from config.database import database
from models.users import UserDB
from models.mytology import MytologyDB
from models.gods import GodsDB
from models.history import HistoryDB

class CommentsDB(Model):
    id = AutoField()
    id_user = ForeignKeyField(UserDB, backref='comments')
    comment = CharField()
    date = DateTimeField()
    last_update = DateTimeField()
    likes = IntegerField()
    status = IntegerField()
    god = ForeignKeyField(GodsDB, backref='comments', null=True)
    mytology = ForeignKeyField(MytologyDB, backref='comments', null=True)
    history = ForeignKeyField(HistoryDB, backref='comments', null=True)

    @property
    def user_id(self):
        return self.id_user.id  # Retornando o ID do usuário

    class Meta:
        database = database
        table_name = 'comments'

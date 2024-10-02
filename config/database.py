from peewee import SqliteDatabase

database = SqliteDatabase('database-v2.db')

def startup_db():
    database.connect()

    from models.users import UserDB
    from models.mytology import MytologyDB
    from models.history import HistoryDB
    from models.gods import GodsDB
    from models.comments import CommentsDB

    database.create_tables(
        [
            UserDB,
            MytologyDB,
            HistoryDB,
            GodsDB,
            CommentsDB
        ]
    )

def shutdown_db():
    database.close()
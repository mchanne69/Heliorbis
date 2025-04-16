import sqlite3
from flask import g
from datetime import datetime

create_table = """CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            Date_Created TEXT,
            Last_Login_Date TEXT,
            Num_Login_attempts INTEGER DEFAULT 0,
            Last_PWD_Reset TEXT,
            has_Admin INTEGER DEFAULT 0,
            Account_Active INTEGER DEFAULT 0
        )"""

def init_db(app):
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(app.config['DATABASE'])
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(e=None):
        db = g.pop('db', None)
        if db:
            db.close()

    app.teardown_appcontext(close_db)
    app.get_db = get_db

    with app.app_context():
        db = get_db()
        db.execute(create_table)
        db.commit()

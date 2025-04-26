import sys
import os
import pytest
import sqlite3

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'  # Use in-memory database
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db = app.get_db()
        # Recreate tables
        db.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            Date_Created TEXT,
            Last_Login_Date TEXT,
            Num_Login_attempts INTEGER DEFAULT 0,
            Last_PWD_Reset TEXT,
            has_Admin INTEGER DEFAULT 0,
            Account_Active INTEGER DEFAULT 0
        )
        """)
        db.commit()

    client = app.test_client()
    yield client

# tests/test_database.py

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import get_config

class TestDatabase(unittest.TestCase):

    def setUp(self):
        app_config = get_config()
        self.app = Flask(__name__)
        self.app.config.from_object(app_config)
        self.db = SQLAlchemy(self.app)

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_sqlite_connection(self):
        with self.app.app_context():
            self.db.create_all()
            # Perform tests for SQLite

    def test_postgresql_connection(self):
        with self.app.app_context():
            # Configure app for PostgreSQL testing
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/test_db'
            self.db.init_app(self.app)
            self.db.create_all()
            # Perform tests for PostgreSQL

if __name__ == '__main__':
    unittest.main()

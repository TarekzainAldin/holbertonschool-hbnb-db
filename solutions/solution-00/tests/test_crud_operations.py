# tests/test_crud_operations.py

import unittest
from src import create_app, db
from src.models.user import User

class TestCRUDOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask app for testing
        cls.app = create_app(config_class="src.config.TestingConfig")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        # Create the database structure
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up after tests
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_create_user(self):
        # Test creating a new user
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)

    def test_read_user(self):
        # Test reading an existing user
        user = User.query.filter_by(username='test_user1').first()
        self.assertEqual(user.email, 'test1@example.com')

    def test_update_user(self):
        # Test updating an existing user
        user = User.query.filter_by(username='test_user1').first()
        user.email = 'updated_email@example.com'
        db.session.commit()

        updated_user = User.query.filter_by(username='test_user1').first()
        self.assertEqual(updated_user.email, 'updated_email@example.com')

    def test_delete_user(self):
        # Test deleting an existing user
        user = User.query.filter_by(username='test_user2').first()
        db.session.delete(user)
        db.session.commit()

        deleted_user = User.query.filter_by(username='test_user2').first()
        self.assertIsNone(deleted_user)

if __name__ == '__main__':
    unittest.main()


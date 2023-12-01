import unittest
from flask import Flask, session
from app import app, db, User

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        with app.app_context():
            db.drop_all()

    def test_login_route(self):
        """Test the /login route."""
        # Create a test user in the database
        with app.app_context():
            test_user = User(name='Test User', email='test@example.com', password='password')
            db.session.add(test_user)
            db.session.commit()

        # Perform a login request
        response = self.app.post('/login', data={'email': 'test@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

        # Check if the session variables are set correctly
        with self.app.session_transaction() as sess:
            self.assertTrue(sess.get('loggedin'))
            self.assertEqual(sess.get('email'), 'test@example.com')

    def test_register_route(self):
        """Test the /register route."""
        # Generate a unique email for testing
        unique_email = 'unique_test_email@example.com'

        # Perform a registration request
        response = self.app.post('/register', data={'name': 'Test User', 'email': unique_email, 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

        # Check if the user is added to the database
        with app.app_context():
            user = User.query.filter_by(email=unique_email).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')

if __name__ == '__main__':
    unittest.main()


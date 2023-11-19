import unittest
from app import app, db, User, Chats
class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and create a test client
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # Clean up the test database
        db.session.remove()
        db.drop_all()

    def test_login_route(self):
        # Test the login route with a valid user
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        # Create a test user
        test_user = User(**user_data)
        db.session.add(test_user)
        db.session.commit()

        # Perform a POST request to the login route with valid credentials
        response = self.app.post('/login', data={'email': user_data['email'], 'password': user_data['password']})

        # Check if the user is redirected to the user route
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/user')

        # Check if the session is set correctly
        with self.app.session_transaction() as sess:
            self.assertTrue(sess['loggedin'])
            self.assertEqual(sess['userid'], test_user.id)
            self.assertEqual(sess['name'], test_user.name)
            self.assertEqual(sess['email'], test_user.email)

    def test_login_route_invalid_credentials(self):
        # Test the login route with invalid credentials
        invalid_user_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }

        # Perform a POST request to the login route with invalid credentials
        response = self.app.post('/login', data=invalid_user_data)

        # Check if the user sees an error message
        self.assertIn(b'Incorrect password. Please try again.', response.data)

        # Check if the session is not set
        with self.app.session_transaction() as sess:
            self.assertNotIn('loggedin', sess)

    def test_register_route(self):
        # Test the register route with valid user data
        new_user_data = {
            'name': 'New Test User',
            'email': 'newtest@example.com',
            'password': 'newtestpassword'
        }

        # Perform a POST request to the register route with valid data
        response = self.app.post('/register', data=new_user_data)

        # Check if the user is redirected to the login page after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

        # Check if the new user is added to the database
        new_user = User.query.filter_by(email=new_user_data['email']).first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.name, new_user_data['name'])

    def test_register_route_existing_user(self):
        # Test the register route with existing user data
        existing_user_data = {
            'name': 'Existing User',
            'email': 'existing@example.com',
            'password': 'existingpassword'
        }

        # Create an existing user
        existing_user = User(**existing_user_data)
        db.session.add(existing_user)
        db.session.commit()

        # Perform a POST request to the register route with existing user data
        response = self.app.post('/register', data=existing_user_data)

        # Check if the user sees an error message
        self.assertIn(b'Account already exists! Please log in.', response.data)

        # Check if a new user is not added to the database
        new_user = User.query.filter_by(email=existing_user_data['email']).first()
        self.assertIsNone(new_user)

    def test_register_route_invalid_email(self):
        # Test the register route with invalid email
        invalid_email_data = {
            'name': 'Invalid Email User',
            'email': 'invalidemail',
            'password': 'invalidemailpassword'
        }

        # Perform a POST request to the register route with invalid email
        response = self.app.post('/register', data=invalid_email_data)

        # Check if the user sees an error message
        self.assertIn(b'Invalid email address! Please enter a valid email.', response.data)

        # Check if a new user is not added to the database
        new_user = User.query.filter_by(email=invalid_email_data['email']).first()
        self.assertIsNone(new_user)

    def test_user_route_authenticated(self):
        # Test the user route for an authenticated user
        authenticated_user_data = {
            'name': 'Authenticated User',
            'email': 'authuser@example.com',
            'password': 'authuserpassword'
        }

        # Create an authenticated user
        authenticated_user = User(**authenticated_user_data)
        db.session.add(authenticated_user)
        db.session.commit()

        # Log in the user
        with self.app.session_transaction() as sess:
            sess['loggedin'] = True
            sess['userid'] = authenticated_user.id
            sess['name'] = authenticated_user.name
            sess['email'] = authenticated_user.email

        # Perform a GET request to the user route
        response = self.app.get('/user')

        # Check if the user sees the correct user data
        self.assertIn(authenticated_user_data['name'].encode(), response.data)

    def test_user_route_unauthenticated(self):
        # Test the user route for an unauthenticated user
        # Perform a GET request to the user route without logging in
        response = self.app.get('/user')

        # Check if the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    # Add more tests for other routes and functionalities as needed

if __name__ == '__main__':
    unittest.main()


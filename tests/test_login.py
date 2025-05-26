# we're using the built-in unittest module to write test cases
import unittest

# we use these to fake database calls and control their behavior
from unittest.mock import patch, MagicMock

# we're importing the flask app from our main.py file so we can send requests to it
from main import app
import main  # this helps us access the global cursor in main.py

# this class will hold all our test cases related to logging in
class TestLoginRoute(unittest.TestCase):

    # this function runs before every single test
    def setUp(self):
        # we create a fake browser (flask test client) so we can simulate GET and POST
        self.client = app.test_client()

        # tell flask we're testing. it helps with error messages
        self.client.testing = True

    # just testing if the login page actually loads
    def test_login_page_loads(self):
        # we fake a get request to /login
        response = self.client.get('/login')

        # we expect a successful load (status 200)
        self.assertEqual(response.status_code, 200)

        # we check if the word "Login" shows up in the HTML page (b means it's in bytes)
        self.assertIn(b'Login', response.data)

    # now we test if someone logs in using valid credentials
    def test_login_with_valid_credentials(self):
        # here's where we fake the DB queries using mock
        # instead of patching, we override the real cursor in main
        main.cursor.execute = MagicMock(side_effect=[
            # 1st query: select password from User
            MagicMock(fetchone=MagicMock(return_value=('test123',))),

            # 2nd query: check if user is admin
            MagicMock(fetchall=MagicMock(return_value=[])),

            # 3rd query: check if user is instructor
            MagicMock(fetchall=MagicMock(return_value=[('testinstructor',)]))
        ])

        # we send the form data using POST to /login
        response = self.client.post('/login', data={
            'username': 'testinstructor',
            'password': 'test123'
        }, follow_redirects=False)

        # since login is successful, we expect (200)
        self.assertEqual(response.status_code, 200)


# this runs all our tests if we launch this file directly
if __name__ == '__main__':
    unittest.main()

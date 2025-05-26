# so here we're using python's unittest library to write a test case
import unittest

# importing our flask app from the main file so we can test its routes
from main import app

# this class is where we write tests related to the instructor dashboard
class TestInstructorDashboard(unittest.TestCase):

    # this runs before each test, we use it to set up a fake browser session
    def setUp(self):
        # creating a test client that lets us send fake requests to the app
        self.client = app.test_client()

        # putting the app in testing mode to get better error messages
        self.client.testing = True

    # this is our actual test to see if the instructor dashboard works properly
    def test_dashboard_access_instructor(self):
        # we're faking a login session here by setting the username and user_type
        with self.client.session_transaction() as sess:
            sess['latte_user'] = 'fakeinstructor'
            sess['user_type'] = 'i'  # 'i' means instructor

        # sending a GET request to the home route which should send us to the instructor dashboard
        response = self.client.get('/')

        # we expect the response to be 200 which means the page loaded successfully
        self.assertEqual(response.status_code, 200)

        # now we're checking if the text "Instructor Dashboard" is somewhere in the page html
        self.assertIn(b'Instructor Dashboard', response.data)

# this just tells python to run the test when we run this file directly
if __name__ == '__main__':
    unittest.main()

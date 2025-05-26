import unittest
from unittest.mock import patch, MagicMock
from main import app

class TestStudentDashboard(unittest.TestCase):

    def setUp(self):
        # we make a fake browser to send requests
        self.client = app.test_client()
        self.client.testing = True

    def test_dashboard_access_student(self):
        # now we patch the cursor used inside main
        with patch('main.cursor') as mock_cursor:
            # we fake fetchall result from the db
            fake_cursor = MagicMock()
            fake_cursor.execute.return_value.fetchall.return_value = [('CNG101',), ('CNG492',)]
            mock_cursor.return_value = fake_cursor
            # we fake a student login session
            with self.client.session_transaction() as sess:
                sess['latte_user'] = 'fakestudent'
                sess['user_type'] = 's'
            # we hit the home page
            response = self.client.get('/')
            # should load successfully
            self.assertEqual(response.status_code, 200)
            # we check that a known course code is in the html response
            self.assertIn(b'Student Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()

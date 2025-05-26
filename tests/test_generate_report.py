import unittest
from main import app
from unittest.mock import patch, MagicMock

class TestGenerateReportPage(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_generate_report_page_loads(self):
        # we patch the cursor used in main.py
        with patch('main.cursor') as mock_cursor:
            # we create a fake cursor
            fake_cursor = MagicMock()
            # when fetchall is called on cursor.execute, return fake course codes
            fake_cursor.execute.return_value.fetchall.return_value = [('CNG101',), ('CNG492',)]
            mock_cursor.return_value = fake_cursor
            # we simulate a logged-in instructor
            with self.client.session_transaction() as sess:
                sess['latte_user'] = 'fakeinstructor'
                sess['user_type'] = 'i'
            # now we access the page
            response = self.client.get('/generate_report')
            # make sure page loads
            self.assertEqual(response.status_code, 200)
            # make sure content shows up
            self.assertIn(b'Generate Report', response.data)

if __name__ == '__main__':
    unittest.main()

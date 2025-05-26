import unittest
from unittest.mock import patch, MagicMock
from main import app

class TestSaveAnswer(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_save_answer_updates_db(self):
        with patch('main.cursor') as mock_cursor:
            with patch('main.conn') as mock_conn:
                # set up mocks
                fake_cursor = MagicMock()
                fake_conn = MagicMock()

                mock_cursor.execute = fake_cursor.execute
                mock_conn.commit = fake_conn.commit

                with self.client.session_transaction() as sess:
                    sess['latte_user'] = 'fakestudent'
                    sess['user_type'] = 's'

                # post to the route
                response = self.client.post('/save_answer/123', data={'answer': 'my_solution'})

                self.assertEqual(response.status_code, 302)

                # manually check execute call
                mock_cursor.execute.assert_called_with(
                    "UPDATE Task SET student_answer=? WHERE task_id=123", ('my_solution',)
                )
                mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()

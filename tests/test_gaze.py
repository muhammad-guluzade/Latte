import unittest

# this code is just an attempt to learn how to use unit test
def process_gaze_data(data):
    if not data:
        return {'fixations': []}
    # Dummy logic for now
    return {'fixations': [{'x': 100, 'y': 200}]}

class TestGazeProcessing(unittest.TestCase):

    def test_empty_data_returns_empty_fixations(self):
        result = process_gaze_data([])
        self.assertEqual(result, {'fixations': []})

    def test_valid_data_returns_fixations(self):
        sample_data = [{'x': 100, 'y': 200, 'timestamp': 1}]
        result = process_gaze_data(sample_data)
        self.assertIn('fixations', result)
        self.assertTrue(len(result['fixations']) > 0)

if __name__ == '__main__':
    unittest.main()

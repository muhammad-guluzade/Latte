import unittest
from main import process_gaze_data

class TestGazeDataProcessing(unittest.TestCase):
    """
    Unit test class for testing the gaze data processing function used in report visualization.
    """
    def test_valid_gaze_data(self):
        """
        Test the function with a typical, valid set of gaze coordinates and timestamps.
        """
        gaze_points = [
            (100, 200, "12:01:00.100 17/04/2025"),
            (105, 205, "12:01:00.300 17/04/2025"),
            (110, 210, "12:01:01.000 17/04/2025"),
        ]

        # Call the function being tested
        result = process_gaze_data(gaze_points)

        # Check that it returned lists of the correct length
        self.assertEqual(len(result["x"]), 3)
        self.assertEqual(len(result["sizes"]), 3)

        # Check that all sizes are numbers (int or float)
        self.assertTrue(all(isinstance(size, float) or isinstance(size, int) for size in result["sizes"]))

    def test_empty_input(self):
        """
        Test the function with an empty list of gaze points.
        """
        gaze_points = []

        # Expect empty outputs when input is empty
        result = process_gaze_data(gaze_points)
        self.assertEqual(result["x"], [])
        self.assertEqual(result["y"], [])
        self.assertEqual(result["sizes"], [])

    def test_invalid_time_format(self):
        """
        Test the function with a badly formatted timestamp to ensure it raises an error.
        """
        gaze_points = [(100, 200, "invalid-time")]

        # Expect the function to raise ValueError due to bad timestamp format
        with self.assertRaises(ValueError):
            process_gaze_data(gaze_points)




# This makes the test script runnable from the command line directly
if __name__ == '__main__':
    unittest.main()

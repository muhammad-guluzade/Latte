
"""In this unit test, we’re checking whether the gaze data processing function works correctly.
The function takes a list of gaze points, filters them based on screen size,
calculates how long the user looked at each point (called fixation duration),
and converts those durations into dot sizes for visualization.
In the first test, we gave it three valid gaze points spaced 200ms apart and checked that the function correctly returned
three x/y positions and three positive sizes.
In the second test,
we gave it an empty list to see if it could handle missing data,
and it passed by returning empty results without crashing.
This test makes sure our gazeplot visualizations will work reliably whether data is available or not."""
import unittest
from utils.report_utils import process_gaze_data

class TestGazeplotProcessing(unittest.TestCase):

    def test_valid_input(self):
        # this is a normal case with valid gaze points and timestamps
        coordinates = [
            (120, 250, "10:00:00.000"),
            (122, 251, "10:00:00.200"),
            (125, 255, "10:00:00.400"),
        ]
        width, height = 800, 600
        left, top = 100, 200

        result = process_gaze_data(coordinates, width, height, left, top)

        self.assertEqual(len(result["x"]), 3)
        self.assertEqual(len(result["y"]), 3)
        self.assertEqual(len(result["sizes"]), 3)
        self.assertTrue(all(s > 0 for s in result["sizes"]))

    def test_empty_input(self):
        coordinates = []
        result = process_gaze_data(coordinates, 800, 600, 100, 200)
        self.assertEqual(len(result["x"]), 0)
        self.assertEqual(len(result["y"]), 0)
        self.assertEqual(result["sizes"], [])
        self.assertEqual(result["timestamps"], [])

if __name__ == "__main__":
    unittest.main()

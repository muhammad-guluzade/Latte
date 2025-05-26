import unittest
from IVT import apply_ivt

class TestIVTAlgorithm(unittest.TestCase):

    # this is a normal test where the gaze is moving slowly and should count as fixation
    def test_valid_fixation(self):
        gaze_data = [
            (100, 100, "10:00:00.000"),
            (102, 101, "10:00:00.050"),
            (103, 102, "10:00:00.100")
        ]
        fixations = apply_ivt(gaze_data)
        self.assertEqual(len(fixations), 1)  # we expect 1 fixation
        self.assertAlmostEqual(fixations[0][0], 103)  # x average
        self.assertAlmostEqual(fixations[0][1], 102)  # y average

    # here the movement is very fast so it shouldn't count as a fixation
    def test_fast_movement(self):
        gaze_data = [
            (100, 100, "10:00:00.000"),
            (500, 500, "10:00:00.050")
        ]
        fixations = apply_ivt(gaze_data)
        self.assertEqual(len(fixations), 0)  # no fixation should be detected

    # here the timestamp is invalid and should be skipped
    def test_invalid_timestamp(self):
        gaze_data = [
            (100, 100, "10:00:00.000"),
            (105, 105, "INVALID_TIME")
        ]
        fixations = apply_ivt(gaze_data)
        self.assertEqual(len(fixations), 0)  # no valid pair to test

if __name__ == '__main__':
    unittest.main()

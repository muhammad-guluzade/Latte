# utils/report_utils.py

import numpy as np
import datetime

# this function processes gaze data and returns x, y, sizes, timestamps
def process_gaze_data(coordinates, width, height, left, top):
    gaze_x = np.array([])
    gaze_y = np.array([])
    raw_times = []

    for x, y, t in coordinates:
        if 0 <= x - left < width and 0 <= y - top < height:
            gaze_x = np.append(gaze_x, x - left)
            gaze_y = np.append(gaze_y, y - top)
            raw_times.append(t.split()[0])

    if len(raw_times) < 2:
        return {"x": gaze_x, "y": gaze_y, "sizes": [], "timestamps": []}

    timestamps = [datetime.datetime.strptime(t, "%H:%M:%S.%f") for t in raw_times]

    fixation_durations = [max(50, (timestamps[i + 1] - timestamps[i]).total_seconds() * 1000)
                          for i in range(len(timestamps) - 1)]
    fixation_durations.append(fixation_durations[-1])  # repeat last one

    sizes = np.interp(fixation_durations, (min(fixation_durations), max(fixation_durations)), (100, 500))

    return {"x": gaze_x, "y": gaze_y, "sizes": sizes, "timestamps": timestamps}

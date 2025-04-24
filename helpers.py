# helpers.py

from datetime import datetime
import numpy as np

def process_gaze_data(gaze_points):
    """
    Processes gaze data into x, y coordinates, fixation durations, and size values.
    """
    gaze_x = []
    gaze_y = []
    timestamps = []

    for x, y, t in gaze_points:
        t = t.split()[0]  # Remove date if present
        gaze_x.append(x)
        gaze_y.append(y)
        timestamps.append(datetime.strptime(t, "%H:%M:%S.%f"))

    fixation_durations = [
        max(50, (timestamps[i + 1] - timestamps[i]).total_seconds() * 1000)
        for i in range(len(timestamps) - 1)
    ]
    if fixation_durations:
        fixation_durations.append(fixation_durations[-1])
    else:
        fixation_durations.append(100)

    min_size, max_size = 100, 500
    sizes = np.interp(fixation_durations, (min(fixation_durations), max(fixation_durations)), (min_size, max_size))

    return {
        "x": gaze_x,
        "y": gaze_y,
        "sizes": sizes.tolist(),
        "timestamps": timestamps
    }

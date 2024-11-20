import os
from datetime import datetime, timedelta
import joblib

# Determine timestamp for each frame
def frame_timestamp(folder_name):
    # Paremeters set in rosbag2video.py
    fps = 25      # Frames per second
    rate = 1.0
    timestamp_str = folder_name.split('_')[0]  # e.g. '2024-08-22-15-10-50'
    folder_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d-%H-%M-%S')
    folder_path = f'../test_data/{folder_name}' 
    # List all files in the folder and filter out only frame files (structure 'frame_000000.png')
    frame_files = [f for f in os.listdir(folder_path) if f.startswith('frame_') and f.endswith('.png')]

    # Sort frame files 
    frame_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    # interval between frames (in seconds)
    frame_interval_seconds = 1 / fps
    # Adjust for playback rate
    frame_interval_seconds *= rate

    # Calculate timestamps for each frame
    frame_timestamps = []
    for i, frame in enumerate(frame_files, start=1):
        # Calculate the timestamp for this frame by adding the frame interval
        timestamp_for_frame = folder_timestamp + timedelta(seconds=(i - 1) * frame_interval_seconds)
        frame_timestamps.append((frame, timestamp_for_frame))
    return frame_timestamps

def linear_interpolate(t1, t2, data1, data2, t):
    """
    Perform linear interpolation between two data points.
    t1, t2 : Timestamps of first/second data point
    data1: First data point (latitude, longitude)
    data2: Second data point (latitude, longitude)
    t: The target timestamp for interpolation
    """
    # Calculate the time difference
    delta_t = (t2 - t1).total_seconds()
    if delta_t == 0:
        return data1  # No interpolation needed if timestamps are the same

    # Calculate the ratio of the time difference
    ratio = (t - t1).total_seconds() / delta_t

    # Interpolate between data points
    lat = data1[0] + ratio * (data2[0] - data1[0])
    lng = data1[1] + ratio * (data2[1] - data1[1])
    
    return lat, lng

data_path = '../test_data'
frame_folder = "2024-08-22-15-35-05_folder"

# get vehicle data from test_data
coordinates = joblib.load("../test_data/veh_data1")
list2 = joblib.load("../test_data/veh_data2")
coordinates.extend(list2)

# To enable linear interpolation
linear = False

# get for each frame their timestamp and find start/end time of the video
frame_time = frame_timestamp(frame_folder)
start_time = frame_time[0][1]
end_time = frame_time[-1][1]

# Find vehicle data from start to end time
veh_data = []
# Structure of element: (lat, lng, speed, timestamp)
for element in coordinates:
    if start_time <= element[3] <= end_time:
        veh_data.append((element[3], element[0], element[1]))


frame_veh_gps = []

if linear:
    # Idea 1: Linear Interpolation between two points
    for name, time in frame_time:
    # Find the two closest vehicle data points
        prev_data = None
        next_data = None
        for i in range(1, len(veh_data)):
            if veh_data[i][0] >= time:
                next_data = veh_data[i]
                prev_data = veh_data[i - 1]
                break

        if prev_data and next_data:
            # Interpolate between the two closest data points
            lat, lng = linear_interpolate(prev_data[0], next_data[0], (prev_data[1], prev_data[2]), (next_data[1], next_data[2]), time)
            frame_veh_gps.append((name, time, lat, lng))
        else:
            # If no valid vehicle data, you might want to handle this case (e.g., use the first or last data)
            frame_veh_gps.append((name, time, None, None))
else:
    # Idea 2: Find closest veh_data to given timestamp
    for name, time in frame_time:
        # Find the closest veh_data timestamp
        closest_data = min(
            veh_data, 
            key=lambda vd: abs((vd[0] - time).total_seconds())
        )
        # Add the associated data to the result
        frame_veh_gps.append((name, time, closest_data[1], closest_data[2]))

joblib.dump(frame_veh_gps, data_path+"/gps_per_frame")
# Output the result
#for r in frame_veh_gps:
#    print(r)
print("GPS Coordinates retrived for all frames")
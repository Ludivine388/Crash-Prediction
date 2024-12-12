import joblib
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta


# Pedestrian coordinates
frame_folder = "2024-08-22-15-35-05_folder"
ped_coord_path = f'../test_data/pedestrian_gps/{frame_folder}/ped_gps_per_frame'
ped_coordinates = joblib.load(ped_coord_path)
# Vehicle coordinates 
veh_coordinates = joblib.load(f"../test_data/veh_gps_per_frame/{frame_folder}/gps_per_frame")

#Set simulation crash to True to forward trajectory of pedestrian in time
simulation = False
simulation_time = 5   #seconds

# Haversine Formula to calculate the distance between two gps points -> can be used in our test case for flat surface on the road
def haversine_formula(lat1, lng1, lat2, lng2):
    # Radius of the Earth in meters
    R = 6371000 
    # Convert latitude and longitude from degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, [float(lat1), float(lng1), float(lat2),float(lng2)])
    # Haversine formula
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # Distance in meters
    distance = R * c
    return distance

if simulation:
    # Loop through vehicle coordinates
    for frame_name, timestamp, lat_veh, lng_veh in veh_coordinates:
        # Calculate pedestrian timestamp by adding simulation time
        crash_simulation = timestamp + timedelta(seconds=simulation_time)
        # Find the frame number corresponding to the crash_simulation timestamp
        closest_frame_number = None
        min_time_diff = float('20')  # Starts with a big difference

        for simulation_frame_name, simulation_timestamp, _, _ in veh_coordinates:
            time_diff = abs(simulation_timestamp - crash_simulation).total_seconds()
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_frame_number = int(simulation_frame_name.split('_')[1].split('.')[0])
        
        if closest_frame_number is not None and closest_frame_number in ped_coordinates:
            lat_ped, lng_ped = ped_coordinates[closest_frame_number]
            distance = haversine_formula(lat_veh, lng_veh, lat_ped, lng_ped)
            print(f"Distance: {distance:.2f} m")
            
            # CRASH SIMULATION
            if distance <= 1:
                print("DANGER: CRASH")
        else:
            print(f"Frame {frame_name} does not have a matching entry in the dictionary.")
else:
    # Loop through vehicle coordinates and calculate distance between veh and ped
    for frame_name, timestamp, lat_veh, lng_veh in veh_coordinates:
        # Extract frame number from frame name
        frame_number = int(frame_name.split('_')[1].split('.')[0])
        if frame_number in ped_coordinates:
            lat_ped, lng_ped = ped_coordinates[frame_number]
            distance = haversine_formula(lat_veh, lng_veh, lat_ped, lng_ped)
            print(f"Distance: {distance:.2f} m")
            # CRASH SIMULATION
            if distance <= 5.5:
                print("DANGER: CRASH")
        else:
            print(f"Frame {frame_name} does not have a matching entry in the dictionary.")

    

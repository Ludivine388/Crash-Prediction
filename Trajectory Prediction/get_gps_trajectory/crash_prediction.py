import joblib
from math import radians, sin, cos, sqrt, atan2

# Vehicle coordinates 
veh_coordinates = joblib.load("../test_data/gps_per_frame")

# Pedestrian coordinates
frame_folder = "2024-08-22-15-35-05_folder"
ped_coord_path = f'../test_data/pedestrian_gps/{frame_folder}/ped_gps_per_frame'
ped_coordinates = joblib.load(ped_coord_path)

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

    

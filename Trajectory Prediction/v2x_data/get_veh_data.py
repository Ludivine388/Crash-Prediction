'''
This code processes V2X files located in test_data and returns a concise list of important elements: 
GPS coordinates, speed, and timestamp, stored in gpslist
The V2X data files were retrieved from an OBU installed on an eBike. 
However, the timestamps provided by the OBU are invalid due to an issue with the device. 
In this code, the correct timestamp for each block of received values is calculated based on 
the GPS coordinates, speed, and the log file's creation time.
'''

from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import joblib

def process_vehicle_data(file_path):   
    data = []
    print(f'Processing folder : {file_path}')
    with open(file_path, 'r') as file:
        content = file.read()
    # split content in blocks
    blocks = content.split('</ucuItsStationDetails>')
    for block in blocks: 
        split_block = block.split()         # split by all spaces
        try:
            # Extract the lastRec, lat, and lng values from : lastRec=\"2024-08-22T13:27:34.624Z\"><pos lat=\"49.00942\" lng=\"8.409467\"
            # to extract speed value, find index of split_block item where speed is in content and i+1 is index of speed value : 'lenConf=\\"noTrailerPresent\\"/><speed', 'value=\\"0.03\\"',
            # next() -> first string where condition is true 
            speed_index = [i for i, s in enumerate(split_block) if 'speed' in s][0]    # first item speed value is at the beginning of the block
            speed = split_block[speed_index + 1].split('\\"')[1]        
            lat = next(s for s in split_block if 'lat' in s).split('\\"')[1] 
            lng = next(s for s in split_block if 'lng' in s).split('\\"')[1]     
            lastRec = next(s for s in split_block if 'lastRec' in s).split('\\"')[1] 
            #print(speed, lat, lng, lastRec)                      
            data.append((speed, lat, lng, lastRec))
        # Empty blocks appears during split and are handled with 
        except :
                print("Skipping following empty block:", block)           
    return data

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

def calc_time_between_points(points_list, savePath, timestamp):
    result = []
    time = []

    # lastrec is given as ISO 8601 format and timestamp parameter as string
    timestamp = datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%fZ")
    for i in range(1, len(points_list)):
        speed, lat, lng, lastrec = points_list[i]
        # Calculate distance from the previous point
        prev_speed, prev_lat, prev_lng, prev_lastrec = points_list[i - 1]
        distance = haversine_formula(prev_lat, prev_lng, lat, lng)  # in meters
        # Calculate time difference using speed (given in m/s)
        if float(speed) > 0.0:
            # time_diff in seconds
            time_diff = distance / float(speed)
            time.append(time_diff)
        else:
            # This time_diff was calculated based on result from get_average_time.py
            time_diff =  0.567
            # Check if coordinates are equal for speed = 0
            # print(prev_lat, lat, prev_lng, lng)
        timestamp += timedelta(seconds=time_diff)
        # Append values to result
        result.append((lat, lng, speed, timestamp)) 
    joblib.dump(result, savePath)
    return result

paths = [('../test_data/vehicle_data_1.txt','2024-08-21T15:23:16.000000Z', '../test_data/veh_data1'), 
         ('../test_data/vehicle_data_2.txt', '2024-08-22T15:31:53.000000Z', '../test_data/veh_data2')]


for path, creation_time, output in paths:
    print(path, output, creation_time)
    veh_data = process_vehicle_data(path)
    result = calc_time_between_points(veh_data, output, creation_time)

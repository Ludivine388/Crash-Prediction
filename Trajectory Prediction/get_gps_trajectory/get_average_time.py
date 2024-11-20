'''
This code calculates the average time taken to write a new block of values.
The accurate timestamps are from the OBU mounted on the robot.
'''

from datetime import datetime

def process_vehicle_data(file_path):   
    data = []
    print(f'Processing file : {file_path}')
    with open(file_path, 'r') as file:
        content = file.read()
    # split content in blocks
    blocks = content.split('</ucuItsStationDetails>')
    for block in blocks: 
        split_block = block.split()         # split by all spaces
        try:
            # Extract the lastRec, lat, and lng values from : lastRec=\"2024-08-22T13:27:34.624Z\"><pos lat=\"49.00942\" lng=\"8.409467\"
            # to extract speed value, find index of split_block item where speed is in content and i+1 is index of speed value : 'lenConf=\\"noTrailerPresent\\"/><speed', 'value=\\"0.03\\"',   
            lastRec = next(s for s in split_block if 'lastRec' in s).split('\\"')[1] 
            #print(speed, lat, lng, lastRec)                      
            data.append((lastRec))
        # Empty blocks appears during split and are handled with 
        except :
                print("Skipping following empty block:", block)  

    time_diff_list = []
    for i in range(1, len(data)):
        t1 = datetime.strptime(data[i-1], "%Y-%m-%dT%H:%M:%S.%fZ")
        t2 = datetime.strptime(data[i], "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Calculate the time difference in seconds
        time_diff = (t2 - t1).total_seconds()
        #print(time_diff)
        # Append the time difference to the list
        time_diff_list.append(time_diff)   
    print('average:', sum(time_diff_list)/len(time_diff_list))
    return time_diff_list

process_vehicle_data('../test_data/log_station_details-ARI-OBU.txt')
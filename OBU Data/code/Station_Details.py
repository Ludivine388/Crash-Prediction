# -----------------------------------------------------------
# Code to retrieve Details of all units with their IDs
# -----------------------------------------------------------

import requests
import json
import Station_List

# url of service
url = "http://192.168.20.10:10987/ucuStationDetails"
while True:
    # list of IDs to process
    ID = Station_List.list_all_IDs
    print(ID)
    for station in ID:
        # id of vehicle
        raw_data = '<ucuGetStationDetails statID="' + station + '" />'
        # get StationDetails with given ID
        r = requests.post(url, data=raw_data, headers={'Content-Type': 'application/json'})

        data = r.text
        # save data to log
        file = open('log_station_details.txt', 'a')
        # Append the JSON data to the file
        json.dump(data, file)
        # Add a newline character to separate entries (optional)
        file.write('\n \n \n')
        # Close the file
        file.close()

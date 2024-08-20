# -----------------------------------------------------------
# Code to retrieve all IDs of unit
# -----------------------------------------------------------

import requests
import xml.etree.ElementTree as ET


# url of service
url = "http://192.168.20.10:10987/ucuStationList"

# get xml data from service ucuStationList
response = requests.post(url, headers={'Content-Type': 'application/xml'})
list_station = response.text.split("<vehs>")[1].split("</vehs>")[0].split("<veh")

delimiter = '<veh'
list_all_IDs = []
# add all station ID to list for processing in Station_Details.py
for item in list_station[1:]:
    tree = ET.ElementTree(ET.fromstring(delimiter + item))
    root = tree.getroot()
    list_all_IDs.append(root.attrib['statId'])


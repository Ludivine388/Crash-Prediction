'''
This code generates a satellite map visualization for each GPS coordinate and timestamp from the V2X data. 
'''

import requests
import os
import joblib
from PIL import Image, ImageDraw

# Output folder for images
output_folder = "../test_data/map_images"
os.makedirs(output_folder, exist_ok=True)

# List of coordinates
coordinates = joblib.load("../test_data/veh_data1")
list2 = joblib.load("../test_data/veh_data2")
coordinates.extend(list2)

# Base URL for OSM static maps
base_url = "https://static-maps.yandex.ru/1.x/"

# Parameters documentation in : https://yandex.com/dev/staticapi/doc/en/
for i, (lat, lng, speed, timestamps) in enumerate(coordinates):
    params = {
        "ll": f"{lng},{lat}",       # Longitude, Latitude (OpenStreetMap order)
        "z": 19,                    # Zoom level 
        "size": "650,450",          # Image size 
        "l": "sat",                 # Map layer type: "sat" (satellite)
        "pt": f"{lng},{lat},vkgrm"  # Marker at the GPS point
    }
    response = requests.get(base_url, params=params)
    
    # HTTP status -> OK
    if response.status_code == 200:
        # Save the image
        image_path = os.path.join(output_folder, f"map_{i+1}.png")
        with open(image_path, "wb") as file:
            file.write(response.content)
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            text_pos =  (10,10)
            draw.text(text_pos, str(timestamps), fill="white")
            img.save(image_path)
        print(f"Saved map image: {image_path}")
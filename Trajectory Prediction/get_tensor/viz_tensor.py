'''
Code creates video from png tensor files and saves it as output.mp4 
'''

import cv2
import os
import re

def create_video_from_images(image_folder, output_video_file, frame_rate):
    # Get the list of all image files in the folder (consider only frame_xxxxxx.png images)
    pattern = re.compile(r'^frame_\d{6}\.png$')
    images = [img for img in os.listdir(image_folder) if pattern.match(img)]
    
    # Sort images in the correct order
    images.sort()

    # Retrieve size of the first image
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Save as mp4 video
    video = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))

    # Add each image to the video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Release the video writer object
    video.release()

    print(f"Video saved as {output_video_file}")

image_folder = '../test_data/Tensor_visualization/2024-08-22-15-35-05_folder'  # Folder containing PNG images
output_video_file = "output_video.mp4"  # Output video file path and name (change name if needed)
frame_rate = 5  # Frame rate 

# Create the video
create_video_from_images(image_folder, output_video_file, frame_rate)

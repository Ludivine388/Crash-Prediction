
# Introduction
Creation of Tensor data and visualization:
- `generateTensor.py` : This code computes the 3D coordinates of each pedestrian pose on a pixel-coordinates basis.
-  `generateTensor_Kalman.py` : This code computes the 3D coordinates of each pedestrian pose on a pixel-coordinates basis with an integrated Kalman filter for values correction
Visualization in video:
- `viz_tensor.py` : Code creates video from png tensor visualization and saves it as output.mp4 
  

# Data
Assuming that all the pose and depth data are stored in the folder `../test_data/poseData/pose/{frame_folder}/`, `../test_data/depthImg/{frame_folder}/`. \
Specify the folder you want to process, go to line 15 in `generateTensor.py` and update the folder name as follows:
```
frame_folder = '2024-08-22-15-35-05_folder'          
```

For the video visualization: \
Change the following parameters (line 36-38):
```
image_folder = '../test_data/Tensor_visualization/2024-08-22-15-35-05_folder'  # Folder containing PNG images
output_video_file = "output_video.mp4"  # Output video file path and name (change name if needed)
frame_rate = 5  # Frame rate
```


# Usage
Assuming all the setup requirements are respected and your virtual environment is activated, run:
```
python generateTensor.py
python generateTensor_Kalman.py
python viz_tensor.py
```


# Output
The generated tensor data and visualization for each frame will be saved in:
+ `../test_data/Tensor_visualization/(Kalman)/{frame_folder}`: for visualization
+ `../test_data/InitTensor/(Kalman)/{frame_folder}/`: for tensor data

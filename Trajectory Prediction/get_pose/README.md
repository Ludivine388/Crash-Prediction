# Introduction
This code generates pose value of detected persons in video frames. \
For additional details, refer to the Github repository : [Pytorch-OpenPose](https://github.com/Hzzone/pytorch-openpose)

# Data
Assuming that all the data is stored in the folder `../test_data/frame_folder`. \
To specify the folder you want to process, go to line 40 in `get_pose.py` and update the folder name as follows:
```
frame_folder = '2024-08-22-15-35-05_folder'          
```

# Usage
Assuming all the setup requirements are respected and your virtual environment is activated, run:
```
python get_pose.py
```


# Output
The generated depth map for each frame will be saved in:
+ `../test_data/poseData/img/frame_folder`: for visualization
+ `../test_data/poseData/pose/frame_folder`: for pose data


# Acknowledgements
```
@inproceedings{cao2017realtime,
  author = {Zhe Cao and Tomas Simon and Shih-En Wei and Yaser Sheikh},
  booktitle = {CVPR},
  title = {Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields},
  year = {2017}
}
@inproceedings{simon2017hand,
  author = {Tomas Simon and Hanbyul Joo and Iain Matthews and Yaser Sheikh},
  booktitle = {CVPR},
  title = {Hand Keypoint Detection in Single Images using Multiview Bootstrapping},
  year = {2017}
}
@inproceedings{wei2016cpm,
  author = {Shih-En Wei and Varun Ramakrishna and Takeo Kanade and Yaser Sheikh},
  booktitle = {CVPR},
  title = {Convolutional pose machines},
  year = {2016}
}
```

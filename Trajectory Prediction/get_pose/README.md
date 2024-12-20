# Introduction
This code generates pose value of detected persons in video frames. \
For additional details, refer to the Github repository : [Pytorch-OpenPose](https://github.com/Hzzone/pytorch-openpose)

# Download the Models
Download the two models : body_pose_model.pth and hand_pose_model.pth from:
* [dropbox](https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0)
* [baiduyun](https://pan.baidu.com/s/1IlkvuSi0ocNckwbnUe7j-g)
* [google drive](https://drive.google.com/drive/folders/1JsvI4M4ZTg98fmnCZLFM-3TeovnCRElG?usp=sharing)

Download the pytorch models and put them in a directory named `model` in the pose folder.

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
The generated pose data and visualization for each frame will be saved in:
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

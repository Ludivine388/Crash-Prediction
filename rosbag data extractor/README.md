# Introduction

This code is a simple data extractor from rosbag files.

```text
Portions of this code are adapted from:
Maximilian Laiacker 2020
post@mlaiacker.de
with contributions from
Abel Gabor 2019,
Bey Hao Yun 2021
baquatelle@gmail.com,
beyhy94@gmail.com
a.j.blight@leeds.ac.uk

Repository:
https://github.com/mlaiacker/rosbag2video/blob/master/rosbag2video.py
```

## Requirements 
This code was run and tested with the following installation:
+ ROS Noetic (https://wiki.ros.org/noetic/Installation/Ubuntu)
+ Python 3.8.10
+ Pillow (pip install Pillow)
+ ffmpeg (sudo apt install ffmpeg)


## Parameters and Usage
```
rosbag2video.py [--fps 25] [--rate 1.0] [-o outputfile] [-v] [-s] [-t topic] rosbag_path

--fps   Sets FPS value that is passed to ffmpeg
            Default is 25.
-h      Displays this help.
--ofile (-o) sets output file name.
        If no output file name (-o) is given the filename 'output.mp4' is used.
--rate  (-r) You may slow down or speed up the video.
        Default is 1.0, that keeps the original speed.
-s      Shows each and every image extracted from the rosbag file.
--topic (-t) Only the images from topic "topic" are used for the video output.
```

Simply run:
```bash
python3 rosbag2video.py first_rosbag.bag
```

## Output
The output data can be found in:
+ /your_directory/frame_folders/rosbag_name : for frame_folder
+ /your_directory/mp4_video/rosbag_name : for mp4 output video

# Introduction
This code analyzes video frames and generates a depth map for each one. \
For additional details, refer to the article: "[Learning the Depths of
Moving People by Watching Frozen People](https://mannequin-depth.github.io/)."


# Data
Assuming that all the data is stored in the folder `../test_data/frame_folder`. \
To specify the folder you want to process, go to line 41 in `get_depth.py` and update the folder name as follows:
```
frame_folder = '2024-08-22-15-35-05_folder'              # Name of folder to process
```

# Usage
Assuming all the setup requirements are respected and your virtual environment is activated, run:
```
python get_depth.py
```

# Output
The generated depth map for each frame will be saved `../test_data/depthImg/frame_folder`.

# Acknowledgements
```text
@article{li2019learning,
  title={Learning the Depths of Moving People by Watching Frozen People},
  author={Li, Zhengqi and Dekel, Tali and Cole, Forrester and Tucker, Richard
    and Snavely, Noah and Liu, Ce and Freeman, William T},
  journal={arXiv preprint arXiv:1904.11111},
  year={2019}
}
```

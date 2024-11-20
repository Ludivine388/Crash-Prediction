"""
This code analyzes video frames and generates a depth map for each one.

Code is adapted for only single_view input from:
@article{li2019learning,
  title={Learning the Depths of Moving People by Watching Frozen People},
  author={Li, Zhengqi and Dekel, Tali and Cole, Forrester and Tucker, Richard
    and Snavely, Noah and Liu, Ce and Freeman, William T},
  journal={arXiv preprint arXiv:1904.11111},
  year={2019}
}"""

import torch
import os
from options.train_options import TrainOptions
from loaders import aligned_data_loader
from models import pix2pix_model

BATCH_SIZE = 1

opt = TrainOptions().parse()  # set CUDA_VISIBLE_DEVICES before import torch

# create video_list.txt : text file with path to all the frames 
def create_video_list_txt(folder_path, output_file):
    # Check if the output file exists, create if not
    if not os.path.exists(output_file):
        open(output_file, 'w').close()  # Create an empty file
        # Open the file in write mode
        with open(output_file, 'w') as f:
            # Loop through all files in the folder
            for file in os.listdir(folder_path):
                # Check if the file has a .png/.jpg extension
                # if file.endswith('.jpg'):
                if file.endswith('.png'):
                    # Get the full file path
                    full_path = os.path.join(folder_path, file)
                    # Write the full path to the file with a newline
                    f.write(full_path + '\n')


frame_folder = '2024-08-22-15-35-05_folder'              # Name of folder with all frames
folder_path = '../test_data/'+frame_folder               # folder should be in test_data
output_file = '../test_data/'+frame_folder+'_list.txt'   
create_video_list_txt(folder_path, output_file)          # create list of paths

video_list = output_file

# Load data and information
video_data_loader = aligned_data_loader.DataLoader(video_list, BATCH_SIZE)
video_dataset = video_data_loader.load_data()
print('=================================== Video dataset #images = %d ===================================' %
      len(video_data_loader))

# Model for depth calculation
model = pix2pix_model.Pix2PixModel(opt)

torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True

print(
    '===================================  BEGIN VALIDATION ==================================='
)

print('TESTING ON VIDEO')

model.switch_to_eval()
save_path = '../test_data/depthImg/'

for i, data in enumerate(video_dataset):
    print(i)
    stacked_img = data[0]
    targets = data[1]
    model.run_and_save(stacked_img, targets, save_path)

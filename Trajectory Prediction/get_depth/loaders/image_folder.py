# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import h5py
import torch.utils.data as data
import numpy as np
import torch
import os
import os.path
from skimage import transform
from skimage.io import imread


def make_dataset(list_name):
    text_file = open(list_name, 'r')
    images_list = text_file.readlines()
    text_file.close()
    images_list = [os.path.join(os.getcwd(), i) for i in images_list]
    return images_list


class ImageFolder(data.Dataset):

    def __init__(self, list_path):
        # creates list with all the paths to the images
        img_list = make_dataset(list_path)
        if len(img_list) == 0:
            raise(RuntimeError('Found 0 images in: ' + list_path))
        self.list_path = list_path
        self.img_list = img_list
        
        #Size parameters
        self.resized_height = 480
        self.resized_width = 640

    #Converts and resizes the images
    def load_imgs(self, img_path):
        img = imread(img_path)
        img = np.float32(img)/255.0
        img = transform.resize(img, (self.resized_height, self.resized_width))

        return img

    def __getitem__(self, index):
        targets_1 = {}

        h5_path = self.img_list[index].rstrip()
        img = self.load_imgs(h5_path)

        # converts from np array to PyTorch tensor
        final_img = torch.from_numpy(np.ascontiguousarray(
            img).transpose(2, 0, 1)).contiguous().float()

        targets_1['img_1_path'] = h5_path

        return final_img, targets_1

    def __len__(self):
        return len(self.img_list)

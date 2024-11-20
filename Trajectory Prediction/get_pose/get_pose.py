"""
This code determines pose value of detected persons in video frames
This code was simplified and adapted for our test case based on:
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
}"""

import cv2
import copy
import os
import glob
import joblib
import numpy as np

from pose.src import model
from pose.src import util
from pose.src.body import Body
from pose.src.hand import Hand

body_estimation = Body('pose/model/body_pose_model.pth')
hand_estimation = Hand('pose/model/hand_pose_model.pth')

# Data to process
frame_folder = "2024-08-22-15-35-05_folder"
video_dir = f'../test_data/{frame_folder}/'
# Output folders
savePath_img = f'../test_data/poseData/img/{frame_folder}/'
savePath_pose = f'../test_data/poseData/pose/{frame_folder}/'

# Create output folders if needed
os.makedirs(savePath_img, exist_ok=True)
os.makedirs(savePath_pose, exist_ok=True)

# Function
# Get pixel-wise coordinates of body pose
def getPose(candidate, subset):
    X = []
    Y = []
    # Iterate over each body part index (0 to 17)
    for i in range(18):
    # Iterate over each detected person in the subset
        for n in range(len(subset)):        
            index = int(subset[n][i])
            # If the index is -1, it means the body part was not detected
            if index == -1:
                X.append(-1)  
                Y.append(-1)  
                continue  
            # If the index is valid, retrieve the corresponding x and y coordinates
            x, y = candidate[index][0:2]  
            X.append(x) 
            Y.append(y) 
    X_ = []
    Y_ = []
    # Number of person detected:
    total_p = len(X)//18
    for i in range(total_p):
        # coordinates of body parts per person
        x=[] 
        y=[]
        for j in range(18):
            index = j + i * 18
            x_, y_ = X[index], Y[index]
        # Check if both coordinates are valid (not -1)
            if x_ != -1 and y_ != -1:
                x.append(x_)  
                y.append(y_) 
        # Convert the temporary lists to NumPy arrays and append to X_ and Y_
        X_.append(np.array(x))  
        Y_.append(np.array(y))  
    # Convert the lists of arrays to NumPy arrays for output
    # Try function needed for different sizes of array
    try:
        X_ = np.array(X_)  
        Y_ = np.array(Y_)
    except ValueError:
        X_ = np.array(X_, dtype=object)
        Y_ = np.array(Y_, dtype=object)
    return X_,Y_

# Main script
imgnames = sorted(glob.glob(os.path.join(video_dir, "*.png")), key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
total = len(imgnames)
print(f'=================================== {total} images to process ===================================')
for num, test_image in enumerate(imgnames):
    oriImg = cv2.imread(test_image)  # B,G,R order
    # subset: n*20 array, 0-17 is the index in candidate, 18 is the total score, 19 is the total parts
    # candidate: per list : x, y, score, id
    candidate, subset = body_estimation(oriImg)
    #For tests:
    #if not len(subset) == 0:
    #    print(num)
    #    print(subset)
    #    print(candidate)

    canvas = copy.deepcopy(oriImg)
    # get bodypose
    canvas = util.draw_bodypose(canvas, candidate, subset)
    
    # detect hand
    hands_list = util.handDetect(candidate, subset, oriImg)
    all_hand_peaks = []
    for x, y, w, is_left in hands_list:
        peaks = hand_estimation(oriImg[y:y+w, x:x+w, :])
        peaks[:, 0] = np.where(peaks[:, 0]==0, peaks[:, 0], peaks[:, 0]+x)
        peaks[:, 1] = np.where(peaks[:, 1]==0, peaks[:, 1], peaks[:, 1]+y)
        all_hand_peaks.append(peaks)

    # Pose visualization
    canvas = util.draw_handpose(canvas, all_hand_peaks)
    output_filename = f'{savePath_img}/frame_'+str(num).zfill(6)+'.png'
    cv2.imwrite(output_filename, canvas)

    X,Y = getPose(candidate, subset)

    if X.size == 0:  # Check if X is empty
        # Create empty binary image 
        print(f"No pose estimation for frame {num}. Saving empty pose data.")
        empty_pose_data = np.zeros((oriImg.shape[0], oriImg.shape[1]))   
        joblib.dump(empty_pose_data, savePath_pose + "frame_" + str(num).zfill(6) + ".pose")
        continue

    DATA = []
    if len(X.shape) > 2:
        print(X)
    for k in range(X.shape[0]):    # Loop through each detected person's pose data
        # create blank binary image
        data = np.zeros((oriImg.shape[0], oriImg.shape[1]))  
        for i in range(len(X[k])):  # Loop through each keypoint
            x = int(X[k][i])  
            y = int(Y[k][i]) 
            r = 2  # Define a radius for the keypoint representation
            for i in range(-r, r, 1):  
                for j in range(-r, r, 1):  
                    # Check boundaries to avoid index errors
                    if 0 < (y + i) < 480 and 0 < (x + j) < 640:
                        # Set value to 1 for valid location
                        data[y + i][x + j] = 1  
        data = cv2.resize(data, (640, 480), interpolation=cv2.INTER_NEAREST) 
        DATA.append(data)
    DATA = np.array(DATA)
    # To check binary as image (savePath_pose2 needs to be created):
    # image_path = os.path.join(savePath_pose2, f'image_{num}.png')
    # cv2.imwrite(image_path, data * 255)
    # Save binary pose information 
    joblib.dump(DATA, savePath_pose + "frame_" + str(num).zfill(6) + ".pose")  # Save pose data to file
    print("GeneratePose:{}".format(str(num).zfill(6) + ".pose with size:{}".format(DATA.shape))) 
print(f'=================================== Process finished ===================================')

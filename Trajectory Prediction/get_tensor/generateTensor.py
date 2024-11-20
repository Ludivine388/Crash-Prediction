"""
This code computes the 3D coordinates of each pedestrian pose on a pixel-by-pixel basis
"""

import cv2
import joblib
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Change only frame_folder to process another file
frame_folder = "2024-08-22-15-35-05_folder"
depthImgPath = f'../test_data/depthImg/{frame_folder}/'
poseDataPath = f'../test_data/poseData/pose/{frame_folder}/'
savePath = f'../test_data/InitTensor/{frame_folder}/'
savePath_img = f'../test_data/Tensor_visualization/{frame_folder}'

# Creates output paths if needed
os.makedirs(savePath, exist_ok=True)
os.makedirs(savePath_img, exist_ok=True)

# Collecting and sorting files by numbers
depthImgFilenames = sorted(glob.glob(os.path.join(depthImgPath, "*.png")),
                       key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
PoseDataFilenames = sorted(glob.glob(os.path.join(poseDataPath, "*.pose")),
                       key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
# for testing:
#depthImgFilenames = ['../test_data/depthImg/2024-08-22-15-16-10_folder/frame_000130.png']
#PoseDataFilenames = ['../test_data/poseData/pose/2024-08-22-15-16-10_folder/frame_000130.pose']

TENSOR = []
total = len(depthImgFilenames)
print(f'=================================== {total} images to process ===================================')
for num in range(len(depthImgFilenames)):
    pose = joblib.load(PoseDataFilenames[num])

    # Check if pose is empty
    if np.all(pose == 0):
        print(f"Skipping empty pose for file: {PoseDataFilenames[num]}")
        TENSOR.append([(num, 0, 0, 0)])
        continue

    dataShape = pose.shape

    # Handle the case where there are multiple persons (n, 480, 640)
    if len(dataShape) == 3:
        num_persons = dataShape[0]
    else:
        num_persons = 1
        pose = np.expand_dims(pose, axis=0)  

    depth_oriImg = cv2.imread(depthImgFilenames[num])

    # Keep only the depth part of the image and one channel and rescale
    height, width = depth_oriImg.shape[:2]
    depthImg = depth_oriImg[:, width // 2:width] 
    depthImg = depthImg[:, :, 0] 
    depthImg = cv2.normalize(depthImg, None, 0, 250, cv2.NORM_MINMAX)

    # Save a frame as depth visualization with colors
    # frame number 100 is chosen for pedestrian view (other frames can be empty, at the beginning of the video)
    if num == 100:
        plt.figure(figsize=(8,6))
        plt.imshow(depthImg, cmap='jet')  # Use a colormap for better visual representation
        plt.colorbar(label='Depth Scale (0 to 250)')  # Add color bar for scale
        plt.title('Depth Image with Scale')
        plt.axis('off')  # Hide axes for better visualization

        # Save the image with the color scale
        plt.savefig(f'{savePath_img}/depth_scale.png', bbox_inches='tight')
        plt.close()

    # Create and Save 3D Plot with Average Depth Information ---
    fig_3d = plt.figure()
    ax_3d = fig_3d.add_subplot(111, projection='3d')

    for person_idx in range(num_persons):
        current_pose = pose[person_idx, :, :]  # Get the current person's pose data

        # Get the U, V coordinates 8pixelwise coordinates
        V_coords, U_coords = np.where(current_pose == 1)

        if len(U_coords) == 0 or len(V_coords) == 0:
            continue  # No keypoints detected, skip

        D_vals, U_vals, V_vals = [], [], []
        depth_values = []

        for (v, u) in zip(V_coords, U_coords):
            # Ensure that U and V stay within expected limits
            if 0 <= u < 640 and 0 <= v < 480:
                # Store the depth value from the depth image 
                depth_value = 250 - depthImg[v, u]  # Invert the depth value!!
                # depth_value = depthImg[v, u]
                depth_values.append(depth_value)

        # Calculate average depth 
        if len(depth_values) > 0:
            avg_depth_value = np.mean(depth_values)  

        for (v, u) in zip(V_coords, U_coords):
            # Apply the same average depth_value for all keypoints
            D_vals.append(avg_depth_value)  # Depth -> for X-axis
            U_vals.append(u)                # U -> for Y-axis
            V_vals.append(height - v)       # Inverted V -> for Z-axis 
 
        ax_3d.scatter(D_vals, U_vals, V_vals)

        # Append depth, u, v values to tensor
        TENSOR.append([(num, d, u, v) for d, u, v in zip(D_vals, U_vals, V_vals)])

    # 3D plot
    ax_3d.set_xlim(0, 250)  
    ax_3d.set_ylim(0, 640)  
    ax_3d.set_zlim(0, 480)  
    ax_3d.set_xlabel('D (Depth)')
    ax_3d.set_ylabel('X (Horizontal)')
    ax_3d.set_zlabel('Y (Vertical)')
    ax_3d.set_title(f'3D Pose Visualization - Frame {num}')
    ax_3d.legend()

    # Save the 3D plot as a PNG file
    save_filename_3d = f'{savePath_img}/frame_' + str(num).zfill(6) + '.png'
    print("GenerateTensor:{}".format(str(num).zfill(6)))
    plt.savefig(save_filename_3d)
    plt.close(fig_3d)  # Close the figure to avoid displaying it inline if not needed
joblib.dump(TENSOR, savePath+"Tensor")
print(f'=================================== Process finished ===================================')

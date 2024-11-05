import cv2
import joblib
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

frame_folder = "2024-08-22-15-16-10_folder"
depthImgPath = f'../test_data/depthImg/{frame_folder}/'
poseDataPath = f'../test_data/poseData/pose/{frame_folder}/'
savePath = f'../test_data/InitTensor/{frame_folder}/'
savePath_img = f'../test_data/test2/{frame_folder}/tensor_visualisation'

os.makedirs(savePath, exist_ok=True)
os.makedirs(savePath_img, exist_ok=True)

depthImgFilenames = sorted(glob.glob(os.path.join(depthImgPath, "*.png")),
                       key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
PoseDataFilenames = sorted(glob.glob(os.path.join(poseDataPath, "*.pose")),
                       key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
# for testing:
#depthImgFilenames = ['../test_data/depthImg/2024-08-22-15-16-10_folder/frame_000130.png']
#PoseDataFilenames = ['../test_data/poseData/pose/2024-08-22-15-16-10_folder/frame_000130.pose']

TENSOR = []
total = len(depthImgFilenames)
print(f'=================================== {total} to process ===================================')
for num in range(len(depthImgFilenames)):
    pose = joblib.load(PoseDataFilenames[num])

    # Check if pose is empty
    if np.all(pose == 0):
        print(f"Skipping empty pose for file: {PoseDataFilenames[num]}")
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

    # Create and Save 3D Plot with Average Depth Information ---
    fig_3d = plt.figure()
    ax_3d = fig_3d.add_subplot(111, projection='3d')

    for person_idx in range(num_persons):
        current_pose = pose[person_idx, :, :]  # Get the current person's pose data

        # Get the X, Y coordinates 
        Y_coords, X_coords = np.where(current_pose == 1)

        if len(X_coords) == 0 or len(Y_coords) == 0:
            continue  # No keypoints detected, skip

        D_vals, X_vals, Y_vals = [], [], []
        depth_values = []

        for (y, x) in zip(Y_coords, X_coords):
            # Ensure that X and Y stay within expected limits
            if 0 <= x < 640 and 0 <= y < 480:
                # Store the depth value from the depth image 
                depth_value = 250 - depthImg[y, x]  # Invert the depth value!!
                depth_values.append(depth_value)

        # Calculate average depth 
        if len(depth_values) > 0:
            avg_depth_value = np.mean(depth_values)  

        for (y, x) in zip(Y_coords, X_coords):
            # Apply the same average depth_value for all keypoints
            D_vals.append(avg_depth_value)  # Depth -> for X-axis
            X_vals.append(x)                # X -> for Y-axis
            Y_vals.append(height - y)       # Inverted Y -> for Z-axis 
 
        ax_3d.scatter(X_vals, Y_vals, D_vals, alpha=0.7)

        # Append depth tensor
        TENSOR.append(list(zip(D_vals, X_vals, Y_vals)))

    # 3D plot
    ax_3d.set_xlim(0, 640)  
    ax_3d.set_ylim(0, 480)  
    ax_3d.set_zlim(0, 250)  
    ax_3d.set_xlabel('X (Horizontal)')
    ax_3d.set_ylabel('D (Depth)')
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
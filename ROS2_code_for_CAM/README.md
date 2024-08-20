#### Prerequisites:
Please follow the [ROS2 Documentation](https://docs.ros.org/en/humble/Installation.html) to install ROS2 Humble.
You can find there Tutorials to create workspaces, packages and build them.

#### Pacakges
In this folder, you can find two ROS2 Packages:
+ [cam_msg](https://github.com/Ludivine388/Crash-Prediction/tree/main/ROS2_code_for_CAM/cam_msg) :
  creates a standardized [ETSI ITS](https://www.etsi.org/deliver/etsi_en/302600_302699/30263702/01.03.01_30/en_30263702v010301v.pdf) CAM message.
+ [py_pubsub](https://github.com/Ludivine388/Crash-Prediction/tree/main/ROS2_code_for_CAM/py_pubsub) :
  creates a publisher and subscriber node in python to pass the information of the CAM in ROS2 Messages.

#### py_pubsub :
This package used for testing an [XML file]( containing informations about a vehicle and given by an OBU Unit. 
The XML file was first parsed in [get_values.py](https://github.com/Ludivine388/Crash-Prediction/blob/main/ROS2_code_for_CAM/py_pubsub/py_pubsub/get_values.py) and then processed in [assign_values.py](https://github.com/Ludivine388/Crash-Prediction/blob/main/ROS2_code_for_CAM/py_pubsub/py_pubsub/assign_values.py) and [values_parameters.py](https://github.com/Ludivine388/Crash-Prediction/blob/main/ROS2_code_for_CAM/py_pubsub/py_pubsub/values_parameters.py) as the format of the variables and values was not in a standardized CAM format.
The output of [assign_values.py](https://github.com/Ludivine388/Crash-Prediction/blob/main/ROS2_code_for_CAM/py_pubsub/py_pubsub/assign_values.py) was used as ROS2_message to be published.
For more details on publisher, subscriber packages see : [ROS2 Tut](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

#### Build and run the packages
+ Step 1:
  Create a ROS2 workspace : <br>
  ```bash
  mkdir ws_code_for_CAM && cd ws_code_for_CAM && mkdir src
+ Step 2:
  In your src folder paste the needed packages
+ Step 3:
  Build all or only specifics packages and then source the setup file <br>
  ```bash
  colcon build
  colcon build --packages-select package_to_build
  source install/setup.bash
+ Step 4:
  Run cam_msg with:
  ```bash
  ros2 interface show cam_msg/msg/CAM
  ```
  Output should return the whole CAM message with all variables and information
  Or py_pubsub with:
  ```bash
  ros2 run py_pubsub talker
  ros2 run py_pubsub listener    #in a 2nd terminal
  ```
  Output should return a CAM Message with values


  
  

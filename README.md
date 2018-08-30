# dvrk_calibrate

Notification
====================

This work is unofficial, unsupported and in progress in the current location.

Description
====================
This repository has code for using daVinci research kit with ROS

# Author

Radian Azhar Gondokaryono: ragondokaryono@wpi.edu

# Packages

This is a short description of the packages in this repository. The detailed explanations and instructions are available in the packages itself.

# Install dvrk_calibrate and dependencies VRPN and vrpn_client_ros
```
# cd to catkin ws src dir
cd /PATH/TO/CATKIN_WS/src
# clone repo
git clone https://github.com/radianag/dvrk_calibrate.git
git clone https://github.com/ros-drivers/vrpn_client_ros.git
# Install vrpn dependency
sudo apt-get update
rosdep install --from-paths .
# build
cd ..
catkin_make
```

# Running Software
 Launch vrpn_client_ros which publishes vrpn packages as ros topics:
 ```
 roslaunch vrpn_client_ros sample.launch server:=<ip_of_server_machine>
 ``` 
<ip_of_server_machine> is IP address of the motive computer software. Should see connected to RigidBody# ...  
In another terminal, run robot and calibration:
```
 rosrun dvrk_calibrate calibrate_psms.py
 ```
 Done, outputs RCM positions and rotations of each robot in camera frame. 

# Dependencies
vrpn_client_ros, vrpn, dvrk_robot (specifically dvrk_python)

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
This package uses optical trackers to calibrate the RCM position and rotation of any PSM/ECM manipulator of the da Vinci Research Kit. 

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
# Test Setup

# Setting up Motive to Stream VRPN
After camera calibration, select 3 markers in group, right-click -> create rigid bodies. Rigid bodies will be oriented to global frame. Click view -> rigid bodies. Click on the rotation rigid bodies. Reorient the axis visually by changing the pitch, yaw, roll angles. 

# Running Software
 Launch vrpn_client_ros which publishes vrpn packages as ros topics:
 ```
 roslaunch vrpn_client_ros sample.launch server:=<ip_of_server_machine>
 ``` 
<ip_of_server_machine> is IP address of the motive computer software. Should see connected to RigidBody# ...  
Setup the rigid body listener. Open file (dvrk_calibrate)/scripts/calibrate_psms.py. Edit tuples ($name, $rigidbody_number_rotation, $rigid_body_num_position). In another terminal, run robot and calibration:
```
 rosrun dvrk_calibrate calibrate_psms.py
 ```
 Done, outputs RCM positions and rotations of each robot in camera frame. 

# Dependencies
vrpn_client_ros, vrpn, dvrk_robot (specifically dvrk_python)

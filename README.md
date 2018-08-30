# dvrk_calibrate

Notification
====================

This work is unofficial, unsupported and in progress in the current location.

Description
====================
Rospackage to recieve optical tracking data while running robot to calibrate the RCM position and rotation of any PSM/ECM manipulator of the da Vinci Research Kit. 

# Author
Radian Azhar Gondokaryono: ragondokaryono@wpi.edu

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
![Image of test setup](https://github.com/radianag/dvrk_calibrate/blob/master/img/rigid_body.png)

For every manipulator place two rigid bodies:
- rigid_body_rotation: 3 markers placed on joint one of manipulator to describe manipulator rotation. The axis of three markers corresponding to the x-z axis of the manipulator.
- rigid_body_RCM     : 3 markers placed on the parallelogram to calibrate the RCM position

# Setting up Motive to Stream VRPN
In Windows desktop:
After camera calibration, select 3 markers in group, right-click -> Rigid Body -> Create From Selected Markers. Rigid bodies will be oriented to global frame. 

For all rigid_body_rotations: Click View -> Rigid Body Properties. Under the Rigid Bodies Pane, click the Orientation tab. Here, reorient the axis visually by changing the pitch, yaw, roll angles . 

Click View -> Data Streaming. Click Broadcast Frame Data. Note the Network Interface -> Local Interface Value. Scroll down. Under VRPN Streaming Engine tab, make port: 3883. Click Broadcast Frame Data.

# Running Software
In Ubuntu desktop:
 Launch vrpn_client_ros which publishes vrpn packages as ros topics:
 ```
 roslaunch vrpn_client_ros sample.launch server:=<ip_of_server_machine>
 ``` 
<ip_of_server_machine> is IP address of the motive computer software: Local Interface Value. Should see: Connection Established
Creating new tracker RigidBody#. 

Setup the rigid body listener:
Open file (dvrk_calibrate)/scripts/calibrate_psms.py. Edit tuples ($name, $rigid_body_rotation_number, $rigid_body_position_number) corresponding to each manipulator being calibrated. Run dVRK manipulators with ROS. In another terminal, run robot and calibration:
```
 rosrun dvrk_calibrate calibrate_psms.py
 ```
 Done, outputs RCM positions and rotations of each manipulator in camera frame. 

# Dependencies
vrpn_client_ros, vrpn, dvrk_robot (specifically dvrk_python)

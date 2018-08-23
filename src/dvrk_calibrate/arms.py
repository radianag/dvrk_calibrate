#!/usr/bin/env python

from numpy import genfromtxt
import rospy
import numpy as np
import dvrk
import geometry_msgs.msg as gm


class Arms:
    def __init__(self, names):
        self.name = names
        self.pos = np.zeros(3)
        self.rot = np.zeros(4)
        self.arm_rot = np.zeros(4)
        self.marker_data_pos = np.zeros((1, 3))
        self.marker_data_rot = np.zeros((1, 4))

        print(names)
        if self.name[0:3] == 'ECM':
            self.interface = dvrk.ecm(self.name[0])
        else:
            self.interface = dvrk.psm(self.name[0])

        rospy.Subscriber('/vrpn_client_node/RigidBody' + str(self.name[0]) + '/pose', gm.PoseStamped, self.handle_rotation)
        rospy.Subscriber('/vrpn_client_node/RigidBody' + str(self.name[1]) + '/pose', gm.PoseStamped, self.handle_rcm)

    def handle_rotation(self, msg):
        self.arm_rot = np.array([msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w])

    def handle_rcm(self, msg):
        self.pos = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
        self.rot = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]

    def get_marker_data(self):
        self.marker_data_pos = np.append(self.marker_data_pos, [self.pos], axis=0)
        self.marker_data_rot = np.append(self.marker_data_rot, [self.rot], axis=0)

        #self.matrix_rot_rcm = tf.transformations.quaternion_matrix(self.rot_rcm)

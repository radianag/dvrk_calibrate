#!/usr/bin/env python

import rospy
import numpy as np
import tf

from dvrk_calibrate.arms import Arms
import cloudpickle as pickle


class Calibrate:
    def __init__(self, names, limit_psm=[(0.75, 0.75), (0.25, 0.75)], limit_ecm=[(0.75, 0.75), (0.25, 0.75)], rate=100):

        self.names = names
        self.num = len(names)
        self.rate = rate
        self.limit_psm = limit_psm
        self.limit_ecm = limit_ecm

        self.bpost = np.zeros((self.num, 6))
        self.arm_rotations = np.zeros((self.num, 4))

        self._interface()
        self.r = rospy.Rate(self.rate)

        self.r.sleep()
        #print('pose:', self.arm[0].pos)

    def _conca(self, positions, quaternion):
        for i in range(len(quaternion)):
            x = tf.transformations.quaternion_matrix(quaternion[i])
            if i == 0:
                matrix = np.concatenate((x[0:3, 0:3], np.identity(3)), axis=1)
                array = positions[i]
            else:
                y = np.concatenate((x[0:3, 0:3], np.identity(3)), axis=1)
                matrix = np.concatenate((matrix , y), axis=0)
                array = np.append(array, positions[i])

        return array, matrix

    def _interface(self):
        if not rospy.get_node_uri():
            rospy.init_node('calibrate_test', anonymous=True, log_level=rospy.WARN)
        else:
            rospy.logdebug(rospy.get_caller_id() + ' -> ROS already initialized')

        self.arm = [None]*self.num
        for i in range(self.num):
            if self.names[i][0:3] == 'ECM':
                self.arm[i] = Arms(self.names[i])
            else:
                self.arm[i] = Arms(self.names[i])

        rospy.spin()

    def calculate_transform(self, load):
        if load:
            x = 0
        else:
            x = 0

        for x in range(self.num):
            p, f = self._conca(self.arm[x].marker_data_pos, self.arm[x].marker_data_rot)

            j = np.linalg.pinv(f)
            self.bpost[x] = np.matmul(j, -p)
            self.arm_rotations[x] = self.arm[x].arm_rot

    def get_results(self):
        return self.bpost, self.arm_rotations

    def run_test(self, q1_num=10, final_time=2, tool_position=0.05):
        limit_q3 = tool_position

        tf = final_time
        z = q1_num
        z2 = self.rate * tf

        traj_q1 = np.zeros((self.num, z))
        traj_q2 = np.zeros((self.num, z2))

        for i in range(self.num):
            if self.names[i][0:3] == 'ECM':
                self.arm[i].interface.move_joint_some(np.array([self.limit_ecm[0][0], self.limit_ecm[1][0], limit_q3]),
                                                      np.array([0, 1, 2]))

                traj_q1[i] = np.linspace(self.limit_ecm[0][0], self.limit_ecm[0][1], num=z)
                traj_q2[i] = np.linspace(self.limit_ecm[1][0], self.limit_ecm[1][1], num=z2)
            else:

                self.arm[i].interface.move_joint_some(np.array([self.limit_psm[0][0], self.limit_psm[1][0], limit_q3]),
                                                      np.array([0, 1, 2]))

                traj_q1[i] = np.linspace(self.limit_ecm[0][0], self.limit_ecm[0][1], num=z)
                traj_q2[i] = np.linspace(self.limit_ecm[1][0], self.limit_ecm[1][1], num=z2)

        i = 0

        print("I'm here")
        while i < z and not rospy.is_shutdown():
            j = 0
            for x in range(self.num):
                self.arm[x].interface.move_joint_some(np.array([traj_q1[x][i], traj_q2[x][j], limit_q3]), np.array([0, 1, 2]))
                self.arm[x].get_marker_data()

            while j < z2 and not rospy.is_shutdown():
                for x in range(self.num):
                    self.arm[x].interface.move_joint_some(np.array([traj_q1[x][i], traj_q2[x][j], limit_q3]), np.array([0, 1, 2]), False)
                    self.arm[x].get_marker_data()
                self.r.sleep()
                j = j + 1
            i = i + 1

        # p2.move_joint_some(np.array([-0, -0, limit_q3]), np.array([0, 1, 2]))
        # p1.move_joint_some(np.array([-0, -0, limit_q3]), np.array([0, 1, 2]))

    def save_data(self, folder, name):
        data_rot = np.zeros((self.num, 4))
        data_rcm_pos = np.zeros((self.num, len(self.arm[0].marker_data_pos), 3))
        data_rcm_rot = np.zeros((self.num, len(self.arm[0].marker_data_rot), 4))

        for x in range(len(self.num)):
            data_rot[x] = self.arm[x].arm_rot
            data_rcm_pos[x] = self.arm[x].marker_data_pos
            data_rcm_rot[x] = self.arm[x].marker_data_rot

        data = DataStore(self.names, data_rot, data_rcm_pos, data_rcm_rot)
        model_file = folder + name + '.pkl'
        with open(model_file, 'wr') as f:
            pickle.dump(data, f)


class DataStore:
    def __init__(self, names, data_rot, data_rcm_pos, data_rcm_rot):
        self.names = names
        self.data_rot = data_rot
        self.data_rcm_pos = data_rcm_pos
        self.data_rcm_rot = data_rcm_rot


#!/usr/bin/env python

#  Finds transformation matrix for 3 optical markers attached to the mount to calibrate
#  dvrk-psm-force-feedback device
# gives transformation_matrix.txt and transformation_matrix.npz files as an output

from dvrk_calibrate.calibrate import Calibrate
import rospkg
import tf




if __name__ == '__main__':
    x = tf.transformations.quaternion_matrix([0, 0, 0, 1])
    print(x[0:3,0:3])

    names = [('PSM1', 1, 2), ('PSM2', 4, 3)]
    testname = 'one'

    calib = Calibrate(names)
    calib.run_test()

    rospack = rospkg.RosPack()
    path = rospack.get_path('dvrk_calibrate')
    folder = '/data'
    total = path + folder

    calib.calculate_transform(False)

    #calib.save_data(total, testname)



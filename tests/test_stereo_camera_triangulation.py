from cv2 import cv2
import numpy as np


cameraMatrix1 = np.array([[809.883176965966, 0.886034032625625, 316.494186415504],[0, 809.480527551197, 259.479954642016],[0, 0, 1]])
cameraMatrix2 = np.array([[807.831648614680, -0.788391545797257, 272.993913252552],[0,803.864772000702, 246.423205227026],[0, 0, 1]])

distCoeffs1 = np.array([0.0256227635463143, 0.896159980382255, 0.00873083398185427, 0.00873083398185427, -3.25886055005505])
distCoeffs2 = np.array([-0.0369649324852416, 0.938013893397162, -0.000974301696704835, -0.0135007622685574, -2.53552387041851])


imageSize = (720, 480)
R = np.array([[0.994185708978996, 0.0217522029478750, 0.105459080826859],[-0.0233882141594073, 0.999624161679240, 0.0143012875472788],[-0.105108360753868, -0.0166846352669367, 0.994320801072594]])
T = np.array([314.111143461680, -49.9034065181065, 18.4777366882179])

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T)

print(P1)
print(P2)

point1 = np.array([[263., 107.], [100., 0.]])
point2 = np.array([[472., 84.], [100., 0.]])

pt1 = pt2 = 0

pt1	= cv2.undistortPoints(point1, cameraMatrix1, distCoeffs1, None, R1, P1)
pt2	= cv2.undistortPoints(point2, cameraMatrix2, distCoeffs2, None, R2, P2)

points4D = cv2.triangulatePoints(P1, P2, pt1, pt2)

points4D /= points4D[3]

print(points4D)

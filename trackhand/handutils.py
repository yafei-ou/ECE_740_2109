import numpy as np
import math


def fitPlane(points):
    # Fit 3d points to a plane
    xs = points[0, :]
    ys = points[1, :]
    zs = points[2, :]

    # do fit
    tmp_A = []
    tmp_b = []
    for i in range(len(xs)):
        tmp_A.append([xs[i], ys[i], 1])
        tmp_b.append(zs[i])
    b = np.matrix(tmp_b).T
    A = np.matrix(tmp_A)

    # Manual solution
    fit = (A.T * A).I * A.T * b
    errors = b - A * fit
    residual = np.linalg.norm(errors)

    # Or use Scipy
    # from scipy.linalg import lstsq
    # fit, residual, rnk, s = lstsq(A, b)
    # Z[r,c] = fit[0] * X[r,c] + fit[1] * Y[r,c] + fit[2]
    
    return [fit[0, 0], fit[1, 0], fit[2, 0]], residual

def fitLine(points):
    # Fit 3D points to a line
    
    x = points[0, :]
    y = points[1, :]
    z = points[2, :]

    data = np.concatenate((x[:, np.newaxis], 
                        y[:, np.newaxis], 
                        z[:, np.newaxis]), 
                        axis=1)

    # Calculate the mean of the points, i.e. the 'center' of the cloud
    datamean = data.mean(axis=0)

    # Do an SVD on the mean-centered data.
    _, _, vv = np.linalg.svd(data - datamean)

    # Now vv[0] contains the first principal component, i.e. the direction
    # vector of the 'best fit' line in the least squares sense.
    
    directv, mean = vv[0], datamean
    return directv, mean

def getNormalVectorfromPlane(params):
    # Returns the normal vector of a plane Z = Ax + By + C
    # where params = [A, B, C]
    v = [-params[0], -params[1], 1]
    # print(v)
    v = v/np.linalg.norm(v)
    return v

def getRotationMatrixfromVectors(axisY, axisZ):
    # Compute rotation matrix from 2 axis direction vectors Y, Z

    axisX = np.cross(axisY, axisZ) # axisY and axisZ are orthogonal unit vectors
    rotationMatrix = np.array([axisX, axisY, axisZ])
    rotationMatrix = np.dot(np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]]), rotationMatrix)


    return rotationMatrix

def rotationMatrixToEulerAngles(R) :
    
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    
    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])

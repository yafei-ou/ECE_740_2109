from typing import Container
import cv2
import numpy as np
import math
import socket
import struct
import mediapipe as mp
import time
import pickle
import trackhand.threadedcamera as tcam
from trackhand.handdetector import SingleHandDetector
from trackhand import handutils

cap1 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)

cap2 = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)


mpDraw = mp.solutions.drawing_utils

threadedCam1 = tcam.ThreadedCamera(cap1)
threadedCam2 = tcam.ThreadedCamera(cap2)

handDetector1 = SingleHandDetector()
handDetector2 = SingleHandDetector()


## Camera specification
cameraMatrix1 = np.array([[809.883176965966, 0.886034032625625, 316.494186415504],[0, 809.480527551197, 259.479954642016],[0, 0, 1]])
cameraMatrix2 = np.array([[807.831648614680, -0.788391545797257, 272.993913252552],[0,803.864772000702, 246.423205227026],[0, 0, 1]])

distCoeffs1 = np.array([0.0256227635463143, 0.896159980382255, 0.00873083398185427, 0.00873083398185427, -3.25886055005505])
distCoeffs2 = np.array([-0.0369649324852416, 0.938013893397162, -0.000974301696704835, -0.0135007622685574, -2.53552387041851])

fundamentalMat = np.array([[0.000008674844622,0.000022598231401,-0.078615982712994], [0.000029532325372,0.000007571903266,-0.401275325675112], [0.051357997068133,0.380874972580572,10.629690090409383]])

imageSize = (720, 480)
R = np.array([[0.994185708978996, 0.0217522029478750, 0.105459080826859],[-0.0233882141594073, 0.999624161679240, 0.0143012875472788],[-0.105108360753868, -0.0166846352669367, 0.994320801072594]])
T = np.array([314.111143461680, -49.9034065181065, 18.4777366882179])

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T)


## Load svm model
with open('svm.pickle', 'rb') as fr:
    clf = pickle.load(fr)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.0.3', 8005)

pTime = 0
data = []
count = 0
while True:
    success1, img1 = threadedCam1.read()
    success2, img2 = threadedCam2.read()
    if success1 and success2:
        imgRGB1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        imgRGB2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    else:
        continue

    points1 = handDetector1.runDetection(imgRGB1)
    points2 = handDetector2.runDetection(imgRGB2)
    points1 = handDetector1.stabilize()
    points2 = handDetector2.stabilize()

    if points1 and points2:
        points1 = np.array(points1)
        points2 = np.array(points2)
        # print(pt1)
        if handutils.checkOneHand(points1, points2, fundamentalMat):
            # print("one hand")
            for pt1 in points1:
                cx1, cy1 = int(pt1[0]), int(pt1[1])
                cv2.circle(img1, (cx1,cy1), 3, (255,0,255), cv2.FILLED)
            for pt2 in points2:
                cx2, cy2 = int(pt2[0]), int(pt2[1])
                cv2.circle(img2, (cx2,cy2), 3, (255,0,255), cv2.FILLED)
            count += 1
        else:
            count = 0
            img_out = cv2.vconcat([img1, img2])
            img_out = cv2.rotate(img_out, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow("ImageOut", img_out)
            key = cv2.waitKey(5)
            continue
    else:
        count = 0
        img_out = cv2.vconcat([img1, img2])
        img_out = cv2.rotate(img_out, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("ImageOut", img_out)
        key = cv2.waitKey(5)
        continue


    pt1	= cv2.undistortPoints(points1, cameraMatrix1, distCoeffs1, None, R1, P1)
    pt2	= cv2.undistortPoints(points2, cameraMatrix2, distCoeffs2, None, R2, P2)

    points4D = cv2.triangulatePoints(P1, P2, pt1, pt2) # 4x21 matrix, normalized
    points4D /= points4D[3]
    points3D = points4D[0:3, :]

    if count < 5:
        img_out = cv2.vconcat([img1, img2])
        img_out = cv2.rotate(img_out, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("ImageOut", img_out)
        key = cv2.waitKey(5)
        if key & 0xFF == 27:
            break
        continue
    elif count == 5:
        init_point = points3D
    
    ## gesture prediction
    points3D_pred = points3D.copy()
    points_2d = []
    for i in range(3):
        points3D_pred[i, :] = points3D_pred[i, :] - points3D_pred[i, 0]
    points_2d.append(np.delete(points3D_pred, 0, axis=1))
    points_2d = np.reshape(points_2d, (60,))
    pred = clf.predict([points_2d])
    # print(pred)

    if pred[0] == 0.:
        img_out = cv2.vconcat([img1, img2])
        img_out = cv2.rotate(img_out, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("ImageOut", img_out)
        key = cv2.waitKey(5)
        if key & 0xFF == 27:
            break
        continue

    ## Todo: thumb part should be removed when fitting to a plane
    planeParanms, _ = handutils.fitPlane(points3D)
    # print(planeParanms)
    # In Camera Frame, X axis is placed down, Z axis is the direction pointing out of camera.
    # Use right-handed coordinate.
    directionVectorZ = - handutils.getNormalVectorfromPlane(planeParanms)
    directionVectorY, _ = handutils.fitLine(points3D[:, 9:13])
    directionVectorY = - directionVectorY
    [x, y, z] = handutils.rotationMatrixToEulerAngles(handutils.getRotationMatrixfromVectors(directionVectorY, directionVectorZ))


    ## send data through UDP
    message = np.concatenate((points3D[0:3, 9] - init_point[0:3, 9], np.array([x, y, z])))
    # print(message)
    message_UDP = struct.pack('<6d', *message)
    sock.sendto(message_UDP, server_address)
    time.sleep(0.02)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    img_out = cv2.vconcat([img1, img2])
    img_out = cv2.rotate(img_out, cv2.ROTATE_90_CLOCKWISE)
    cv2.putText(img_out,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow("ImageOut", img_out)
    key = cv2.waitKey(5)

    ## save test data
    # if key & 0xFF == 27:
    #     np.save('data.npy', data)
    #     break
    # elif key & 0xFF == 13:
    #     # save data
    #     data.append(points3D)
    
    ## save image
    # if key & 0xFF == 13:
    #     cv2.imwrite("img_out.jpg", img_out)

    ## just quit
    if key & 0xFF == 27:
        break

cap1.release()
cap2.release()


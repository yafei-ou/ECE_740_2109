from threadedcamera import ThreadedCamera
from cv2 import cv2
import numpy as np


# --------------- Camera Parameters and Initialization ---------------
imageWidth = 1280
imageHeight = 720
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth*2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHeight)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

threadedCap = ThreadedCamera(cap)



cameraMatrix1 = np.array([[724.385180103633, 2.74494148191765, 595.665223587459], [
                         0, 723.837790780014, 315.413489420482], [0, 0, 1]])
cameraMatrix2 = np.array([[729.883716911412, 2.83288159285923, 642.492430072632], [
                         0, 729.232844526155, 348.665306017855], [0, 0, 1]])

distCoeffs1 = np.array([0.105050015503242, -0.0599000382934353,
                        0.000731250178132028, -0.000940232668612531, -0.135207976807521])
distCoeffs2 = np.array([0.106083858027303, -0.0748576052789489,
                        0.000042298294016726, -0.00135786818555894, -0.106952370030532])

imageSize = (1280, 720)

R = np.array([[0.999976054595614, -0.00111025734663287, 0.00683063423220888], [0.00109455919025033,
                                                                               0.999996752494893, 0.00230150816807497], [-0.00683316731604127, -0.00229397652405708, 0.999974022410652]])
T = np.array([-59.8866827629306, 0.121836165256864, 0.373971019809084])


cameraParams = [cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T]

# hp = HeadPose(dlib.shape_predictor(
#     "shape_predictor_68_face_landmarks.dat"), threadedCap, cameraParams, isStereo=True, useStabilizer=False)
hp = HeadPose(dlib.shape_predictor(
      "shape_predictor_5_face_landmarks.dat"), threadedCap, cameraParams, isStereo=True, useStabilizer=True, pointsNum=5)

imgCount = 0
while True:
    ret = hp.update()
    if ret:
        currentImg = hp.img
        leftP = hp.currentLeftPoints
        rightP = hp.currentRightPoints

        # 获取左右摄像头的图像
        rgbImageL = currentImg[:, 0:imageWidth, :]
        rgbImageR = currentImg[:, imageWidth:imageWidth * 2, :]
        for i in range(3):
            left = leftP[i]
            right = rightP[i]
            left = (int(left[0]), int(left[1]))
            right = (int(right[0]), int(right[1]))
            print(left)
            cv2.circle(rgbImageL, left, 5, (0, 0, 255), -1)
            cv2.circle(rgbImageR, right, 5, (0, 0, 255), -1)

            
        finalFrame = np.zeros((720, 2560, 3), np.uint8)
        finalFrame[0:720, 0:1280] = rgbImageL
        finalFrame[0:720, 1280:2560] = rgbImageR
        # cv2.imshow('Left', rgbImageL)
        # cv2.imshow('Right', rgbImageR)
        _, angle = hp.getEulerAngles()
        _, position = hp.getPoints3D()
        position = str(np.around(position[0:3, 0]))
        angle = str(np.around(angle[0:]))
        print(position)

        cv2.putText(finalFrame, angle, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(finalFrame, position, (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("final", finalFrame)
        # 按“回车”保存图片
        c = cv2.waitKey(1) & 0xff
        if c == 13:
            # cv2.imwrite('Left%d.bmp' % i, rgbImageL)
            # cv2.imwrite('Right%d.bmp' % i, rgbImageR)
            cv2.imwrite('StereoCamera%d.png' % imgCount, finalFrame)
            print("Save %d image" % imgCount)
            imgCount += 1

    if cv2.waitKey(100) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

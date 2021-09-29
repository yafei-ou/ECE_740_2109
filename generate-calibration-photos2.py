import cv2
import mediapipe as mp
import time
import threadedcamera as tcam
from handdetector import SingleHandDetector, Stabilizer

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

i = 0

while True:
    # 从摄像头读取图片
    success1, rgbImageL = cap1.read()
    success2, rgbImageR = cap2.read()
    if success1 and success2:
        # 获取左右摄像头的图像
        cv2.imshow('Left', rgbImageL)
        cv2.imshow('Right', rgbImageR)
        # 按“回车”保存图片
        c = cv2.waitKey(1) & 0xff
        if c == 13:
            cv2.imwrite('Left%d.bmp' % i, rgbImageL)
            cv2.imwrite('Right%d.bmp' % i, rgbImageR)
            print("Save %d image" % i)
            i += 1

cap.release()
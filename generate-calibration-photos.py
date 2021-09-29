from cv2 import cv2

imageWidth = 1280
imageHeight = 720

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth * 2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHeight)
i = 0

while True:
    # 从摄像头读取图片
    success, img = cap.read()
    if success:
        # 获取左右摄像头的图像
        rgbImageL = img[:, 0:imageWidth, :]
        rgbImageR = img[:, imageWidth:imageWidth * 2, :]
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